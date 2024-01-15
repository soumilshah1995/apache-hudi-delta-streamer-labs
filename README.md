

<img width="952" alt="Screenshot 2023-11-19 at 11 14 55 AM" src="https://github.com/soumilshah1995/apache-hudi-delta-streamer-labs/assets/39345855/80dfe3d2-a11b-4d47-8c67-6f05c5259a54">

# Delta Streamer Series

Welcome to the Delta Streamer Series, a collection of hands-on guides and tutorials for Hudi Streamer (Delta Streamer). In this series, you'll learn various techniques for local ingestion from different sources, including Parquet and CSV. Additionally, explore advanced topics like ingesting data from multiple tables and performing incremental data pulls from Postgres to Hudi using Delta Streamer.

| Title                                                                                                                     | Hyperlink                                |
|---------------------------------------------------------------------------------------------------------------------------|------------------------------------------|
| Hudi Streamer (Delta Streamer) Hands-On Guide: Local Ingestion from Parquet Source #1                                  | [Link](https://www.youtube.com/watch?v=s42-mGktIpg)     |
| Hudi Streamer Delta Streamer Hands On Guide: Local Ingestion from CSV Source #2                                           | [Link](https://www.youtube.com/watch?v=z1NAmGGHbHU)     |
| Learn How to Ingest Multiple Tables using Hudi MultiTable Delta Streamer #3                                              | [Link](https://www.youtube.com/watch?v=mfGb38TQmDY)     |
| RFC-14: Step-by-Step Guide for Incremental Data Pull from Postgres to Hudi using DeltaStreamer (#4)                      | [Link](https://www.youtube.com/watch?v=kqQ0SVwfBig)     |
| Learn How to Ingest Data Into Hudi Table using Delta Streamer in continuous Mode & SQL transformer#5                      | [Link](https://www.youtube.com/watch?v=QVTSKf24heU)     |
| Learn How to use DeltaStreamer and ingest data from Kafka Topic Hands on Labs #6                                          | [Link](https://www.youtube.com/watch?v=uoIpw8lTBV0)     |
| Real-Time Data: Postgres, Debezium, Kafka, Schema Registry, Delta Streamer #7 A                                             | [Link](https://www.youtube.com/watch?v=gypBM9Jpj9I)     |
| Real-Time Data: Postgres, Debezium, Kafka, Schema Registry, Delta Streamer #7B Complete Video                             | [Link](https://www.youtube.com/watch?v=GIs-Y1VYIY8)     |
| Learn How to Run Clustering in Async Mode with Delta Streamer in Continuous Mode  Hands on Labs |#8                       | [Link](https://www.youtube.com/watch?v=7WP4bxj_P3s)     |
| Learn How to use MinIO and Apache Hudi Delta Streamer with Hands on Lab #9                                                 | [Link](https://www.youtube.com/watch?v=bPR17-wvIXI)     |
| How to use DeltaStreamer to Read Data From Hudi Source in Incremental Fashion (Bronze to Silver) #10                      | [Link](https://www.youtube.com/watch?v=MDULTzOmQFA)     |
| Apache Hudi Delta Streamer in Action: Python Publishing and AvroKafkaSource Consumption (#11 Guide)" #11                      | [Link](https://www.youtube.com/watch?v=FSpt4jSH_O0)     |



# Hudi Example Setup

### Step 1: Install PySpark 3.4.0

```bash
pip install pyspark==3.4.0
```

### Step 2: Install Java 11

```
brew install openjdk@11
# For Windows, you can download and install Java 11 from the official website:
# https://adoptopenjdk.net/?variant=openjdk11&jvmVariant=hotspot
```

### Step 3: Install Hadoop 3.7
```
# For macOS:
brew install hadoop@3.7
# For Windows Dollow the Guide
https://www.youtube.com/watch?v=0Quqj3DLC2w
```

### Step 4: Download Dataset and JAR Files
* https://drive.google.com/drive/folders/1BwNEK649hErbsWcYLZhqCWnaXFX3mIsg?usp=share_link
* https://repo.maven.apache.org/maven2/org/apache/hudi/hudi-utilities-slim-bundle_2.12/0.14.0/

### Step 5: Create hudi_tbl.props
```
# Create a file named hudi_tbl.props with the following content:
hoodie.datasource.write.keygenerator.class=org.apache.hudi.keygen.SimpleKeyGenerator
hoodie.datasource.write.recordkey.field=invoiceid
hoodie.datasource.write.partitionpath.field=destinationstate
hoodie.streamer.source.dfs.root=file:///Users/soumilnitinshah/Downloads/sampledata/
hoodie.datasource.write.precombine.field=replicadmstimestamp
```

### Step 6: Create spark-config.properties
```
# Create a file named spark-config.properties with the following content:
spark.serializer=org.apache.spark.serializer.KryoSerializer
spark.sql.catalog.spark_catalog=org.apache.spark.sql.hudi.catalog.HoodieCatalog
spark.sql.hive.convertMetastoreParquet=false
```

#### Step 7: Submit Spark Job
```
# Submit Spark Job
spark-submit \
  --class org.apache.hudi.utilities.streamer.HoodieStreamer \
  --packages org.apache.hudi:hudi-spark3.4-bundle_2.12:0.14.0 \
  --properties-file spark-config.properties \
  --master 'local[*]' \
  --executor-memory 1g \
 jar/hudi-utilities-slim-bundle_2.12-0.14.0.jar \
  --table-type COPY_ON_WRITE \
  --op UPSERT \
  --source-ordering-field replicadmstimestamp \
  --source-class org.apache.hudi.utilities.sources.ParquetDFSSource \
  --target-base-path file:///Users/soumilnitinshah/Downloads/hudidb/ \
  --target-table invoice \
  --props hudi_tbl.props

```
