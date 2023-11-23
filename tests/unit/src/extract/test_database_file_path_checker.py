from unittest.mock import Mock, patch

import pytest
from pyspark import Row

from distributed_pe_processor.database.models.connection_database_data_model import ConnectionDatabaseDataModel
from distributed_pe_processor.src.extract.database_file_path_checker import DatabaseFilePathChecker


def test_construct_query():
    # Setup
    table_name = "table_name"
    db_connection_data = ConnectionDatabaseDataModel(url=None, properties=None,table_name=table_name)
    checker = DatabaseFilePathChecker(spark=None,
                                      db_file_path_column_name='path',
                                      db_connection_data=db_connection_data)
    files = ['file1', 'file2']

    # Exercise
    query = checker.construct_query(files)
    query_to_verify = f"""SELECT path 
                        FROM {table_name} 
                        WHERE path IN ('{files[0]}','{files[1]}')"""
    # Verify
    assert query == query_to_verify

