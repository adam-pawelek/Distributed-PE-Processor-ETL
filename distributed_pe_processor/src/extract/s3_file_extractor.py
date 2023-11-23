import logging

import boto3
import botocore
import pyspark

from distributed_pe_processor.database.models.connection_database_data_model import ConnectionDatabaseDataModel
from distributed_pe_processor.src.extract.database_file_path_checker import DatabaseFilePathChecker


class S3FileExtractor:
    def __init__(self, spark, db_file_path_column_name: str, db_connection_data: ConnectionDatabaseDataModel, logger = logging.getLogger(__name__)):
        self.spark = spark
        self.db_connection_data = db_connection_data
        self.db_file_path_column_name = db_file_path_column_name
        self.logger = logger



    def _get_s3_client(self):
        """Initialize and get S3 client."""
        logging.info("Initializing S3 client")
        return boto3.client('s3', config=boto3.session.Config(signature_version=botocore.UNSIGNED))

    def _get_s3_files(self, s3_client, bucket_name, prefix):
        """Retrieve file paths from S3 bucket."""
        logging.info(f"Retrieving files from bucket: {bucket_name}, prefix: {prefix}")
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        bucket_path = f"s3a://{bucket_name}/"
        for page in page_iterator:
            yield [bucket_path + obj['Key'] for obj in page.get('Contents', [])]

    def _process_s3_file_batch(self, batch_files, files_not_in_db, number_of_files):
        """Process a batch of S3 files and update files_not_in_db list."""
        db_file_path_checker = DatabaseFilePathChecker(
            spark=self.spark,
            db_file_path_column_name=self.db_file_path_column_name,
            db_connection_data=self.db_connection_data,
            logger=self.logger
        )
        files_not_in_db.extend(db_file_path_checker.get_nonexistent_files(batch_files))
        logging.info(f"Number of files not in db: {len(files_not_in_db)}")
        return len(files_not_in_db) >= number_of_files

    def _find_files_not_in_db(self, number_of_files: int, bucket_name: str, prefix: str, batch_size: int = 1000)-> list:
        """
        Retrieve S3 file paths not registered in the local database.\n\n

        Parameters:\n
        - number_of_files (int): Maximum number of file paths to return.\n
        - bucket_name (str): Name of the S3 bucket to scan.\n
        - prefix (str): Prefix path in the S3 bucket to find files.\n
        - batch_size (int, optional): Number of files processed per batch (default: 1000).\n\n

        Returns:\n
        list[str]: List of S3 file paths not found in the local database, limited by `number_of_files`.
        """
        s3_client = self._get_s3_client()
        files_not_in_db = []

        for s3_files in self._get_s3_files(s3_client, bucket_name, prefix):
            # Process in batches
            for i in range(0, len(s3_files), batch_size):
                batch_files = s3_files[i: i + batch_size]
                if self._process_s3_file_batch(batch_files, files_not_in_db, number_of_files):
                    return files_not_in_db[0:number_of_files]

        return files_not_in_db[0:number_of_files]

    def extract_files_not_in_database_from_s3(self, file_limit: int, bucket_name: str, prefix: str,
                                              batch_size: int) -> pyspark.rdd.RDD:
        """
        Extract files from an S3 bucket that are not present in the database.

        Parameters:
        - file_limit (int): The maximum number of files to process.
        - bucket_name (str): The name of the S3 bucket to retrieve files from.
        - prefix (str): The prefix (folder path) in the S3 bucket to look for files.
        - batch_size (int): The number of files to process in a single batch.

        Returns:
        pyspark.rdd.RDD: A Resilient Distributed Dataset (RDD) containing the
            binary data of the extracted files.
        """
        try:
            s3_files = self._find_files_not_in_db(file_limit, bucket_name, prefix, batch_size)
            if not s3_files:
                self.logger.warning("No files found to process")
                return self.spark.sparkContext.emptyRDD()

            files_rdd = self._create_rdd_from_s3_files(s3_files)
            return files_rdd

        except Exception as e:  # Catching specific exception types would be better
            self.logger.error(f"Error reading from bucket: {e}")
            return self.spark.sparkContext.emptyRDD()

    def _create_rdd_from_s3_files(self, s3_files: list[str]) -> pyspark.rdd.RDD:
        """
        Create an RDD from the S3 file paths.

        Parameters:
        - s3_files (List[str]): List of S3 file paths.

        Returns:
        pyspark.rdd.RDD: RDD containing the binary data of the files.
        """
        file_paths = ','.join(s3_files)
        files_rdd = self.spark.sparkContext.binaryFiles(file_paths, minPartitions=100)
        return files_rdd

