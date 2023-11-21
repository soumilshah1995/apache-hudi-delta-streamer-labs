try:
    import os
    import sys
    import pyspark
    from pyspark.sql import SparkSession
    from pyspark import SparkConf, SparkContext
    from faker import Faker
    print("Imports loaded ")
except Exception as e:
    print("Error:", e)

HUDI_VERSION = '0.14.0'
SPARK_VERSION = '3.4'

SUBMIT_ARGS = f"--packages org.apache.hudi:hudi-spark{SPARK_VERSION}-bundle_2.12:{HUDI_VERSION} pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS
os.environ['PYSPARK_PYTHON'] = sys.executable

# Configure Spark session
spark = SparkSession.builder \
    .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') \
    .config('spark.sql.extensions', 'org.apache.spark.sql.hudi.HoodieSparkSessionExtension') \
    .config('className', 'org.apache.hudi') \
    .config('spark.sql.hive.convertMetastoreParquet', 'false') \
    .getOrCreate()

# Define the path
path = "file:///Users/soumilnitinshah/Downloads/hudidb/"

# Read data using Hudi
try:
    hudi_df = spark.read.format("org.apache.hudi").load(path)
    hudi_df.createOrReplaceTempView("hudi_snapshot")
    print("Reading from Spark")

    # Sample query on the Hudi DataFrame
    query = "SELECT salesid, shippingtype, invoiceid FROM hudi_snapshot"
    result_df = spark.sql(query)
    result_df.show()

except Exception as e:
    print("Error while reading from Hudi:", e)
