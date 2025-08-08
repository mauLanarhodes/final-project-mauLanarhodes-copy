import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host='cis2368summer.cidyiu02y2ba.us-east-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='Rental#car1234',
        database='cis2368summerdb',
        connection_timeout=5

    )
# This function returns a connection to the MySQL database using the provided credentials.
# It uses the mysql.connector library to establish the connection.
