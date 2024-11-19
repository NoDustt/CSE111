import sqlite3
from sqlite3 import Error

def databaseConnection():
    database = r"Checkpoint2-dbase.sqlite"
    connection = None
    try:
        connection = sqlite3.connect(database)
        return connection
    except Error as e:
        print(e)
    
    
def closeConnection(connection):
    try:
        connection.close()
    except Error as e:
        print(e)