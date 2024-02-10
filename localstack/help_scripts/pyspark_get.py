from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

BUCKET_NAME = "my-bucket"
ENDPOINT_URL = "http://localhost:4566"
PREFIX = "0/"

# Configure Spark
conf = SparkConf().setAppName("S3RDDApp")
conf.set("spark.hadoop.fs.s3a.endpoint", ENDPOINT_URL)
conf.set("spark.hadoop.fs.s3a.access.key", "your-access-key")
conf.set("spark.hadoop.fs.s3a.secret.key", "your-secret-key")
conf.set("spark.hadoop.fs.s3a.path.style.access", True)
conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

# Initialize Spark Context
sc = SparkContext(conf=conf)

# Initialize Spark Session
spark = SparkSession.builder.config(conf=sc.getConf()).getOrCreate()

# Define the S3 path
s3_path = f"s3a://{BUCKET_NAME}/{PREFIX}"

# Read data into RDD
rdd = sc.textFile(s3_path)

# Example action to verify data
print(rdd.take(10))