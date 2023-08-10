#!/bin/bash

#设置环境变量
#export SPARK_HOME='/usr/local/spark'
#export PYTHONPATH=
#export PYSPARK_PYTHON=

export JAVA_HOME=/usr/local/jdk
export PATH=$PATH:$JAVA_HOME/bin

export HADOOP_HOME=/usr/local/hadoop
export YARN_CONF_DIR=/usr/local/hadoop/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin

input_date=$1
action=$2

if [ -z "$1" ]; then
  input_date=$(date -d '1 day ago' +%Y-%m-%d)
else
  input_date=$1
fi

if [ -z "$2" ]; then
  action="scan"
else
  action=$2
fi

# 校验参数是否为日期
if ! date -d "$input_date" >/dev/null 2>&1; then
  echo "输入参数不是一个有效的日期.默认获取昨天的日期"
  input_date=$(date -d '1 day ago' +%Y-%m-%d)
fi

echo "$input_date" "$action"

mydate=$input_date

/usr/local/spark/bin/spark-submit --master yarn --deploy-mode cluster --name assets_scan \
--py-files ArticleChecker.zip \
--files /usr/local/hive/conf/hive-site.xml \
--archives "hdfs://hdfscluster/spark/application/python_ext/python3.tgz#python3" \
--packages org.apache.hudi:hudi-spark3.3-bundle_2.12:0.13.0 \
-c "spark.dynamicAllocation.enabled=true" \
-c "spark.dynamicAllocation.shuffleTracking.enabled=true" \
-c "spark.dynamicAllocation.initialExecutors=0" \
-c "spark.dynamicAllocation.maxExecutors=1000" \
-c "spark.dynamicAllocation.minExecutors=0" \
-c "spark.pyspark.driver.python=./python3/bin/python3" \
-c "spark.pyspark.python=./python3/bin/python3" \
-c "spark.sql.mapKeyDedupPolicy=LAST_WIN" \
-c "spark.yarn.maxAppAttempts=1" \
/opt/adx/ArticleChecker/scripts/scan.py --date "$mydate"
#-c "spark.executor.memoryOverhead=8g" \
#-c "spark.driver.memory=4g" \
#-c "spark.executor.cores=2" \
#-c "spark.executor.memory=4g" \
