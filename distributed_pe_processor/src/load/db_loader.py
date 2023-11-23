import logging

import pyspark

from distributed_pe_processor.database.models.connection_database_data_model import ConnectionDatabaseDataModel
from distributed_pe_processor.database.models.file_metadata_model import FileMetadataModel


def load_to_db(metadata_rdd: pyspark.rdd.RDD, db_connection_data: ConnectionDatabaseDataModel,  logger = logging.getLogger(__name__)):
    """
    Load file metadata from an RDD to a PostgreSQL database table.\n

    Parameters: \n
    metadata_rdd : rdd
        An RDD containing file metadata.

    db_connection_data : ConnectionDatabaseDataModel
        An instance containing PostgreSQL connection info.
    """
    try:
        column_names = FileMetadataModel.get_dataframe_column_names()
        logger.info(f"Successfully retrieved DataFrame column names: {column_names}")

        metadata_df = metadata_rdd.toDF(column_names)
        logger.info("Converted metadata_rdd to DataFrame.")

        logger.info("Starting to write DataFrame to PostgreSQL...")
        metadata_df.write.jdbc(
            url=db_connection_data.url,
            table=db_connection_data.table_name,
            mode="append",
            properties=db_connection_data.properties

        )
        logger.info(f"Successfully written DataFrame to PostgreSQL table: {db_connection_data.table_name}")

    except Exception as e:
        logger.error(f"Failed to load data to DB. Error: {str(e)}")
        raise

