import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        port=3306,
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME'),

    )
# This function returns a connection to the MySQL database using the provided credentials.
# It uses the mysql.connector library to establish the connection.
