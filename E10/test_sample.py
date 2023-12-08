



try:

    import sys, os, uuid, random
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col
    from pyspark.sql.types import *
    from datetime import datetime
    from faker import Faker
    import datetime
    import time
except Exception as e:
    print("error", e)

global faker

SUBMIT_ARGS = "--packages org.apache.hudi:hudi-spark3.4-bundle_2.12:0.14.0 pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS
os.environ['PYSPARK_PYTHON'] = sys.executable

spark = SparkSession.builder \
    .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') \
    .config('spark.sql.extensions', 'org.apache.spark.sql.hudi.HoodieSparkSessionExtension') \
    .config('className', 'org.apache.hudi') \
    .config('spark.sql.hive.convertMetastoreParquet', 'false') \
    .getOrCreate()

path = "file:///Users/soumilshah/IdeaProjects/SparkProject/DeltaStreamer/hudi/bronze_orders"
print("bronze_orders")
spark.read.format("hudi").load(path).createOrReplaceTempView("bronze_orders")
spark.sql(f"SELECT count(*) FROM bronze_orders ").show()


path = "file:///Users/soumilshah/IdeaProjects/SparkProject/DeltaStreamer/hudi/silver_orders"
print("silver_orders")
spark.read.format("hudi").load(path).createOrReplaceTempView("silver_orders")
spark.sql(f"SELECT count(*) FROM silver_orders ").show()
