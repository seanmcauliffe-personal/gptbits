import snowflake.connector
from typing import List, Dict, Any

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
    connection: snowflake.connector.SnowflakeConnection, 
    query: str
) -> List[Dict[str, Any]]:
    """
    Execute a SQL query on a Snowflake database.
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        # Get column names from the cursor description attribute
        column_names = [column[0] for column in cursor.description]
        # Fetch all rows as dictionaries
        return [dict(zip(column_names, row)) for row in cursor.fetchall()]

def close_connection(
    connection: snowflake.connector.SnowflakeConnection
) -> None:
    """
    Close the connection to a Snowflake database.
    """
    connection.close()

# Usage:
connection = create_connection('USERNAME', 'PASSWORD', 'ACCOUNT_URL', 'WAREHOUSE', 'DATABASE', 'SCHEMA')
results = execute_query(connection, 'SELECT * FROM table_name')
close_connection(connection)
