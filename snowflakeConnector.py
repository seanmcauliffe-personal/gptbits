"""
Module for connecting and interacting with a Snowflake database.
"""

from typing import List, Dict, Any
import snowflake.connector

def create_connection(
    user: str, 
    password: str, 
    account: str, 
    warehouse: str, 
    database: str, 
    schema: str
) -> snowflake.connector.SnowflakeConnection:
    """
    Create a connection to a Snowflake database.
    """
    return snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )

def execute_query(
    conn: snowflake.connector.SnowflakeConnection, 
    query: str
) -> List[Dict[str, Any]]:
    """
    Execute a SQL query on a Snowflake database.
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        # Get column names from the cursor description attribute
        column_names = [column[0] for column in cursor.description]
        # Fetch all rows as dictionaries
        return [dict(zip(column_names, row)) for row in cursor.fetchall()]

def close_connection(
    conn: snowflake.connector.SnowflakeConnection
) -> None:
    """
    Close the connection to a Snowflake database.
    """
    conn.close()

# Usage:
conn = create_connection('USERNAME', 'PASSWORD', 'ACCOUNT_URL', 'WAREHOUSE', 'DATABASE', 'SCHEMA')
results = execute_query(conn, 'SELECT * FROM table_name')
close_connection(conn)

