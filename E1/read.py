import sys
import os


try:
    import os
    import sys
    import pyspark
    from pyspark.sql import SparkSession

    print("Imports loaded")
except Exception as e:
    print("error", e)

HUDI_VERSION = '0.15.0'
SPARK_VERSION = '3.4'

SUBMIT_ARGS = f"--packages org.apache.hudi:hudi-spark{SPARK_VERSION}-bundle_2.12:{HUDI_VERSION} pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS
os.environ['PYSPARK_PYTHON'] = sys.executable

# Set Spark and Hoodie configurations
spark = SparkSession.builder \
    .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') \
    .config('spark.sql.extensions', 'org.apache.spark.sql.hudi.HoodieSparkSessionExtension') \
    .config('spark.sql.hive.convertMetastoreParquet', 'false') \
    .getOrCreate()

path = "file:///Users/soumilshah/IdeaProjects/SparkProject/apache-hudi-delta-streamer-labs/E1/silver"

# Load data and create temporary view
spark.read.format("hudi") \
    .load(path) \
    .createOrReplaceTempView("hudi_snapshot")

spark.sql("SELECT distinct (_hoodie_commit_time) FROM hudi_snapshot ").show(truncate=False)
