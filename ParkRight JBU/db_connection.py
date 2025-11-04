# db_connection.py
import mysql.connector
from mysql.connector import pooling

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',  # Change if not using localhost
    'user': 'root',  # Replace with your MySQL username
    'password': '',  # Replace with your MySQL password
    'database': 'parkrightjbu'  # Database name
}

# Connection Pool
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,  # Adjust based on expected load
        **DB_CONFIG
    )
    print("Database connection successfully.")

except mysql.connector.Error as e:
    print(f"Error creating connection pool: {e}")
    connection_pool = None

def get_db_connection():
    """Fetch a connection from the pool."""
    if connection_pool:
        try:
            return connection_pool.get_connection()
        except mysql.connector.Error as e:
            print(f"Error getting connection from pool: {e}")
    return None

def close_connection(connection):
    """Close a database connection (return to pool)."""
    if connection and connection.is_connected():
        connection.close()
