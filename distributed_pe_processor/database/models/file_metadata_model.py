from dataclasses import dataclass, fields
from typing import Optional


@dataclass
class FileMetadataModel:
    file_path: str
    file_size: int
    file_type: str
    architecture: str
    num_imports: int
    num_exports: int

    @classmethod
    def create_sql_table_script(cls, table_name) -> str:
        # Mapping Python types to SQL types
        type_mapping = {
            str: "TEXT",
            int: "INTEGER",
            Optional[str]: "TIMESTAMP"
        }

        # Generating column definitions dynamically based on the dataclass attributes
        columns_sql = []
        for field in fields(cls):
            sql_type = type_mapping[field.type]
            if field.name == "file_path":
                columns_sql.append(f"{field.name} {sql_type} PRIMARY KEY")
            else:
                columns_sql.append(f"{field.name} {sql_type}")

        # Concatenating the column definitions and creating the full SQL script
        columns_sql_string = ",\n            ".join(columns_sql)
        return f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_sql_string}
        );
        """

    @classmethod
    def get_dataframe_column_names(cls):
        column_name_list = []
        for field in fields(cls):
            column_name_list.append(field.name)

        return column_name_list





    def get_metadata_values_tuple(self):
        values = []
        for field in fields(self):
            values.append(getattr(self, field.name))

        return tuple(values)


'''
# Example usage
my_file = FileMetadataModel(
    file_path='/path/to/file',
    file_size=12345,
    file_type='txt',
    architecture="asdf",
    num_imports=123,
    num_exports=123
)

print(my_file.get_metadata_values_tuple())

#sql_script = my_file.create_sql_table_script()
#sql_script = FileMetadataModel.create_sql_table_script()

sql_script = FileMetadataModel.create_sql_table_script()

print(sql_script)
'''