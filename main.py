import os
import sys
from copy import deepcopy
from dotenv import load_dotenv
from distributed_pe_processor.database.models.connection_database_data_model import ConnectionDatabaseDataModel
from distributed_pe_processor.database.setup.create_tables import setup_db
import logging

from distributed_pe_processor.src.run_etl import run_etl
from utils import spark_creator
from logs.elasticsearch_logger import LogstashHandler
from utils.load_config import load_config


def get_number_files_to_process():
    # Check if the right number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python3 myapp.py [number]")
        sys.exit(1)

    # Try to convert the argument into an integer
    try:
        number_files_to_process = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid integer.")
        sys.exit(1)

    return number_files_to_process


def get_db_connection_data(environment):
    url = f"jdbc:postgresql://{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
    properties = {
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD'),
        "driver": "org.postgresql.Driver"
    }
    metadata_table_name = load_config(environment)["metadata_table_name"]
    db_connection_data = ConnectionDatabaseDataModel(
        url=deepcopy(url),
        properties=deepcopy(properties),
        table_name=deepcopy(metadata_table_name)
    )
    return db_connection_data


def main():
    load_dotenv()
    number_files_to_process = get_number_files_to_process()
    spark = spark_creator.create_spark_session(os.getenv("APP_ENV"))

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.addHandler(LogstashHandler(os.getenv('LOGGER_HOST'), int(os.getenv('LOGGER_PORT'))))
    logger.info("App starts")
    logger.info("Created spark")

    db_connection_data = get_db_connection_data(os.getenv("APP_ENV"))
    setup_db(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        table_name=db_connection_data.table_name
    )
    prefix_list = os.getenv("PREFIX_LIST").split(", ")

    run_etl(
        spark=spark,
        db_connection_data=db_connection_data,
        number_files_to_process=number_files_to_process,
        prefix_list=prefix_list,
        bucket_name=os.getenv('BUCKET_NAME'),
        logger=logger,
        db_file_path_column_name=load_config(os.getenv("APP_ENV"))["db_file_path_column_name"]
    )
    spark.stop()


if __name__ == "__main__":  # pragma: no cover
    main()
