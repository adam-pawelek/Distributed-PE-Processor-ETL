import logging

from distributed_pe_processor.database.models.connection_database_data_model import ConnectionDatabaseDataModel


class DatabaseFilePathChecker:
    def __init__(self, spark, db_file_path_column_name: str, db_connection_data: ConnectionDatabaseDataModel,logger = logging.getLogger(__name__)):
        self.db_file_path_column_name = db_file_path_column_name
        self.db_connection_data = db_connection_data
        self.spark = spark
        self.logger = logger

    def construct_query(self, files):
        """Constructs SQL query string based on the file list."""
        self.logger.info('Constructing query.')
        try:
            files_str = ','.join([f"'{file}'" for file in files])
            query = f"""SELECT {self.db_file_path_column_name} 
                        FROM {self.db_connection_data.table_name} 
                        WHERE {self.db_file_path_column_name} IN ({files_str})"""
        except Exception as e:
            self.logger.error(f'Error constructing query: {str(e)}')
            raise
        return query

    def get_existing_files(self, query):
        """Fetches existing files from the database."""
        logging.info('Fetching existing files from database.')
        try:
            existing_files_df = self.spark.read.jdbc(
                self.db_connection_data.url,
                f"({query}) as tmp",
                properties=self.db_connection_data.properties
            )
            return [row[self.db_file_path_column_name] for row in existing_files_df.collect()]
        except Exception as e:
            logging.error(f'Error fetching existing files: {str(e)}')
            raise

    def get_nonexistent_files(self, files):
        """Returns files that are not present in the database."""
        logging.info('Identifying nonexistent files.')
        try:
            query = self.construct_query(files)
            existing_files = self.get_existing_files(query)

            return set(files) - set(existing_files)
        except Exception as e:
            logging.error(f'Error identifying nonexistent files: {str(e)}')
            raise