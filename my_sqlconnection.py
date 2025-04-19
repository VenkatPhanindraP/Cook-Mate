import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Create a connection to the MySQL database.
    Returns:
        connection: A MySQL connection object.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your DB host, e.g., '127.0.0.1'
            user='root',       # Replace with your MySQL username
            password='password',  # Replace with your MySQL password
            database='cookmate_db'  # Replace with your database name
        )
        if connection.is_connected():
            print("Connected to MySQL Database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def execute_query(connection, query, params=None):
    """
    Execute a given SQL query.
    Args:
        connection: A MySQL connection object.
        query: SQL query string.
        params: Optional tuple of parameters to pass to the query.
    """
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"Error executing query: {e}")

def fetch_results(connection, query, params=None):
    """
    Fetch results from a SELECT query.
    Args:
        connection: A MySQL connection object.
        query: SQL SELECT query string.
        params: Optional tuple of parameters to pass to the query.
    Returns:
        list: Query results.
    """
    try:
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error fetching results: {e}")
        return []

def close_connection(connection):
    """
    Close the MySQL connection.
    Args:
        connection: A MySQL connection object.
    """
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed")
