try:
    import os
    import sys
    import uuid
    import pyspark
    from pyspark.sql import SparkSession
    from pyspark import SparkConf, SparkContext
    from faker import Faker
    import pandas as pd  # Import Pandas library for pretty printing

    print("Imports loaded ")

except Exception as e:
    print("error", e)

HUDI_VERSION = '0.14.0'
SPARK_VERSION = '3.4'

SUBMIT_ARGS = f"--packages org.apache.hudi:hudi-spark{SPARK_VERSION}-bundle_2.12:{HUDI_VERSION} pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS
os.environ['PYSPARK_PYTHON'] = sys.executable

spark = SparkSession.builder \
    .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') \
    .config('spark.sql.extensions', 'org.apache.spark.sql.hudi.HoodieSparkSessionExtension') \
    .config('className', 'org.apache.hudi') \
    .config('spark.sql.hive.convertMetastoreParquet', 'false') \
    .getOrCreate()

path = "file:///Users/soumilshah/IdeaProjects/SparkProject/apache-hudi-delta-streamer-labs/E8/hudidb/orders"
spark.read.format("org.apache.hudi").load(path).createOrReplaceTempView("hudi_snapshot")

spark.sql("SELECT DISTINCT _hoodie_partition_path, _hoodie_commit_time FROM hudi_snapshot").show(10)


query = f"call show_clustering(path => '{path}', show_involved_partition => true);"
df = spark.sql(query)
df.show(truncate=False)

