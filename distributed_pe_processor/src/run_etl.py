import os

from distributed_pe_processor.src.extract.s3_file_extractor import S3FileExtractor
from distributed_pe_processor.src.load import db_loader
from distributed_pe_processor.src.transform import file_transformer


def extract_files_from_s3(spark, extractor, number_files_to_process, prefix_list,bucket_name):
    concatenated_rdd = spark.sparkContext.range(0, 0)
    for prefix in prefix_list:
        new_binary_files_rdd = extractor.extract_files_not_in_database_from_s3(
            file_limit=(number_files_to_process // len(prefix_list)),
            bucket_name=bucket_name,
            prefix=prefix,
            batch_size=1000
        )
        concatenated_rdd = concatenated_rdd.union(new_binary_files_rdd)
    return concatenated_rdd


def run_etl(spark, db_connection_data, number_files_to_process, prefix_list, bucket_name, logger, db_file_path_column_name):
    extractor = S3FileExtractor(spark=spark, db_file_path_column_name=db_file_path_column_name, db_connection_data=db_connection_data,logger=logger)
    binary_files_rdd = extract_files_from_s3(spark=spark, extractor=extractor, number_files_to_process=number_files_to_process, prefix_list=prefix_list, bucket_name=bucket_name)
    metadata_rdd = file_transformer.transform_files_to_metadata(binary_files_rdd=binary_files_rdd, logger=logger)
    db_loader.load_to_db(metadata_rdd=metadata_rdd, db_connection_data=db_connection_data, logger=logger)

