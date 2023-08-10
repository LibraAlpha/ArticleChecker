import sys
import argparse
import hashlib
import configs.redis as redis_config
from pyspark.sql.functions import explode, split, col, udf, when, concat_ws
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, ArrayType, DoubleType
from pyspark import SparkConf, SparkContext
from modules.tools import parse_img_url
from modules.db import mysql_tools
from modules.secret import get_md5_hash
from modules.Asset import Asset

from scripts.load_ad_pos import default_list


class Scanner(object):

    def __init__(self):
        super().__init__()
        self.spark = SparkSession.builder.enableHiveSupport().getOrCreate()
        self.sparkContext = self.spark.sparkContext

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
