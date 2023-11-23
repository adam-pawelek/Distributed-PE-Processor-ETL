from pyspark.sql import SparkSession

from utils.load_config import load_config


def create_spark_session(environment):
    """
    Create and return a Spark session with configurations specified in SPARK_SESSION_CONFIGS.
    """
    spark = SparkSession.builder

    for config_key, config_value in load_config(environment)["spark_session_configs"].items():
        spark = spark.config(config_key, config_value)

    spark = spark.getOrCreate()
    return spark
