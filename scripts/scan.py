import sys
import argparse
import redis
import hashlib
import configs.redis as redis_config
from pyspark.sql.functions import explode, split, col, udf, when, concat_ws
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, ArrayType, DoubleType
from pyspark import SparkConf, SparkContext
from modules.tools import parse_img_url
import modules.db.redis_tools as redis_tools


class Scanner(object):

    def __init__(self):
        super().__init__()
        self.spark = SparkSession.builder.enableHiveSupport().getOrCreate()
        self.sparkContext = self.spark.sparkContext

    """
    redis结构：
    uncensored: {
        assert_url: {
            title: xxx,
            desc: xxx
        }
        another_assert_url: {
            title: xxx,
            desc: xxx
        }
    }
    blocked:{
        assert_url: {
            title: xxx,
            desc: xxx
        }
        another_blocked_assert_url: {
            title: xxx,
            desc: xxx
        }         
    }
    """

    def write_to_redis(self, partition):
        redis_client = redis_tools.get_redis_client()
        for row in partition:
            title_encoded = row['ad_title']  # title与desc可能存在多个，不同广告主之间通过|分割，格式为“广告主id-base64编码内容”
            desc_encoded = row['ad_description']
            img_url = row['img_url']

            title_list = title_encoded.split('|')
            desc_list = desc_encoded.split('|')
            img_url_list = img_url.split('|')

            tmp_list = dict()

            for item_url in img_url_list:
                url_info = item_url.split['|']
                advertizer, img_url_raw = url_info[0], url_info[1]
                processed_img_url = parse_img_url(img_url_raw)
                tmp_list[advertizer]['url'] = processed_img_url
                tmp_list[advertizer]['title'] = ''
                tmp_list[advertizer]['desc'] = ''

            for item_title in title_list:
                title_info = item_title.split('-')
                advertizer, base64_title = title_info[0], title_info[1]
                tmp_list[advertizer]['title'] = base64_title

            for item_desc in desc_list:
                desc_info = item_desc.split('-')
                advertizer, base64_desc = desc_info[0], desc_info[1]
                tmp_list[advertizer]['desc'] = base64_desc

            for key, item in tmp_list.items():
                img_url_raw = item['url']
                title_base64 = item['title']
                desc_base64 = item['desc']



    def scan(self, date, hour=0):
        sql_get_data = """
            select get_json_object(kafka_value, '$.IUL') as img_url,
            get_json_object(kafka_value, '$.AT') as ad_title,
            get_json_object(kafka_value, '$.AD') as ad_description,            
            from wiseadx.ods_data_mor_ro
            where dt = '{0}'
            and h = '{1}';            
        """.format(date, hour)

        df = self.spark.sql(sql_get_data).drop_duplicates().repartition(2000)
        df.foreachPartition(self.write_to_redis)


if __name__ == '__main__':
    analyzer = Analyze()

    parser = argparse.ArgumentParser(description="Arg parser for ctr prediction.")
    parser.add_argument('--date', type=str, help='yyyy-mm-dd format date string')
    parser.add_argument('--action', type=str,
                        help='actions to perform. [verify] for validaion, [pred] for get pred results.')

    args = parser.parse_args()

    action = args.action
    input_date = args.date

    print(input_date, action)

    if action == 'pred':
        analyzer.pred(input_date)
    if action == 'verify':
        analyzer.verify(input_date)
