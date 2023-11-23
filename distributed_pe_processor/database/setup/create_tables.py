import os

import psycopg2
from dotenv import load_dotenv

from distributed_pe_processor.database.models.file_metadata_model import FileMetadataModel


def create_table(cursor,conn, table_name, model = FileMetadataModel):
    # Check if table already exists
    cursor.execute(f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = '{table_name}'
        );
    """)
    table_exists = cursor.fetchone()[0]

    # If table doesn't exist, create it
    if not table_exists:
        sql_script = model.create_sql_table_script(table_name=table_name)
        print(sql_script)
        cursor.execute(sql_script)
        conn.commit()
        print(f"Table '{table_name}' created successfully!")
    else:
        print(f"Table '{table_name}' already exists!")




def setup_db(host: str, dbname: str, user: str, password: str, port: int = 5432, table_name: str = "your_table_name"):
    """
    Create a table with a specified structure if it doesn't exist in a PostgreSQL database.

    Args:
        host (str): Hostname or IP address of the PostgreSQL server.
        dbname (str): Name of the database.
        user (str): Username for the database.
        password (str): Password for the database.
        port (int, optional): Port number for the database. Defaults to 5432.
        table_name (str, optional): Name of the table. Defaults to "your_table_name".
    """

    # Connection string
    conn_string = f"host='{host}' dbname='{dbname}' user='{user}' password='{password}' port='{port}'"
    # Connect to the database
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    create_table(cursor,conn, table_name)

    # Close the connection
    cursor.close()
    conn.close()

