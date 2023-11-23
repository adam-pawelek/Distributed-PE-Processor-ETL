import pytest

from distributed_pe_processor.database.models.file_metadata_model import FileMetadataModel


# Test data
@pytest.fixture
def sample_file():
    return FileMetadataModel(
        file_path='/path/to/file',
        file_size=12345,
        file_type='txt',
        architecture='x86',
        num_imports=10,
        num_exports=5
    )


# Tests
def test_create_sql_table_script():
    sql_script = FileMetadataModel.create_sql_table_script("test_table")

    expected_script = """
    CREATE TABLE IF NOT EXISTS test_table (
            file_path TEXT PRIMARY KEY,
            file_size INTEGER,
            file_type TEXT,
            architecture TEXT,
            num_imports INTEGER,
            num_exports INTEGER
        );
    """

    assert sql_script.strip() == expected_script.strip()


def test_get_dataframe_column_names():
    column_names = FileMetadataModel.get_dataframe_column_names()

    expected_column_names = [
        'file_path',
        'file_size',
        'file_type',
        'architecture',
        'num_imports',
        'num_exports'
    ]

    assert column_names == expected_column_names


def test_get_metadata_values_tuple(sample_file):
    metadata_values = sample_file.get_metadata_values_tuple()

    expected_values = (
        '/path/to/file',
        12345,
        'txt',
        'x86',
        10,
        5
    )

    assert metadata_values == expected_values