import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection



def execute_query(connection, query, params):
    print(params)
    res = None
    cursor = connection.cursor()
    try:

        if len(params) > 0:
            cursor.execute(query, params)
            res = cursor.fetchone() # fetchall()
        else:
            cursor.execute(query)
            # res = cursor.fetchone()
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

    return res

def execute_query_select(connection, query, params):
    print(params)
    res = None
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        res = cursor.fetchall()

        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

    return res

