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
from modules.db import redis_tools
from modules.db import mysql_tools
from modules.secret import get_md5_hash
from modules.Asset import Asset

from scripts.load_ad_pos import default_list


class Scanner(object):

    def __init__(self):
        super().__init__()
        self.spark = SparkSession.builder.enableHiveSupport().getOrCreate()
        self.sparkContext = self.spark.sparkContext

    """
 
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

    def write_to_mysql(self, iterator):
        count = 0
        session = mysql_tools.sessionmaker(bind=mysql_tools.engine)
        for row in iterator:
            asset = Asset()
            asset.url = row.img_url
            asset.title = row.title
            asset.description = row.description
            asset.adv = row.adv
            asset.ad_pos = row.ad_pos
            asset.url_md5 = get_md5_hash(asset_url)
            asset.created_at = row.dt

            count += 1

            if count % 1000 == 0:
                session.commit()

    def scan(self, date):
        get_bid_data = f"""
            select get_json_object(kafka_value, '$.id') as id,
            get_json_object(kafka_value, '$.IUL') as img_url,
            get_json_object(kafka_value, '$.AT') as title,
            get_json_object(kafka_value, '$.AD') as description,
            get_json_object(kafka_value, '$.I') as adpos,
            get_json_object(kafka_value, '$.C') as adv,
            1 as bid            
            from wiseadx.ods_data_mor_ro
            where dt = '{date}'           
            and type='B'
            and get_json_object(kafka_value, '$.IUL') is not null
            and h = '3'            
        """

        get_impression_data = f"""
          select get_json_object(kafka_value, '$.id') as id, 1 as impression                        
            from wiseadx.ods_data_mor_ro
            where dt = '{date}'           
            and type='R'
            and h = '3'   
        """

        get_click_data = f"""
            select get_json_object(kafka_value, '$.id') as id, 1 as click                        
            from wiseadx.ods_data_mor_ro
            where dt = '{date}'           
            and type='C'
            and h = '3'
        """

        bid_data = self.spark.sql(get_bid_data).drop_duplicates().repartition(2000).fillna('None')
        impression_data = self.spark.sql(get_impression_data).drop_duplicates().repartition(2000)
        click_data = self.spark.sql(get_click_data).drop_duplicates().repartition(2000)

        combined = bid_data.join(impression_data, on='id', how='left').join(click_data, on='id', how='left')

        stats = combined.groupBy('adpos', 'adv', 'img_url').agg(
            sum(col('bid')).cast('int').alias('bids'),
            sum(col('impression')).cast('int').alias('impressions'),
            sum(col('click')).cast('int').alias('clicks')
        )

        stats.write.mode('overwrite') \
            .option('header', 'true') \
            .csv('hdfs://hdfscluster/user/hive/warehouse/test.db/export/tag=asset_report.csv')

        return "Done"


if __name__ == '__main__':
    scanner = Scanner()

    parser = argparse.ArgumentParser(description="Arg parser for ctr prediction.")
    parser.add_argument('--date', type=str, help='yyyy-mm-dd format date string')
    # parser.add_argument('--hour', type=str, help='data period')

    args = parser.parse_args()

    input_date = args.date
    hour = args.hour

    print(input_date, hour)

    scanner.scan(date)
