import sqlite3
import pandas as pd
import logging
from sqlite3 import Error
from utils import user_sql_query, admin_sql_query, other
from contextlib import closing

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def create_connection(path):
    try:
        connection = sqlite3.connect(path)
        print("Connected to SQLite DB")
        return connection
    except Error as e:
        logging.error(f"Connection error: {e}")
        return None

def execute_query(connection, query, params=[]):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print("Query executed successfully")
        return cursor.fetchall()
    except Error as e:
        logging.error(f"SQL error: {e}")
        return None

def execute_query_select(connection, query, params=[]):
    return execute_query(connection, query, params)


class SQLiteDB:
    def __init__(self, DBNAME):
        self.DBNAME = DBNAME

    def create_table_users(self, message):
        with create_connection(self.DBNAME) as connection:
            execute_query(connection, user_sql_query.create_table_users)
            execute_query(connection, user_sql_query.save_user, [
                message.from_user.id, 
                message.from_user.username,
                message.from_user.first_name,
                other.get_msk_time()
            ])
    
    def get_user_row(self, from_user_id: int):
        with create_connection(self.DBNAME) as connection:
            connection.row_factory = sqlite3.Row  
            cursor = connection.cursor()
            cursor.execute(user_sql_query.get_user_row, [from_user_id])
            row = cursor.fetchone()
            return dict(row) if row else None

    def find_elements_by_keyword(self, table_name: str, key_name: str, column_name: str):
        with create_connection(self.DBNAME) as connection:
            query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?"
            return execute_query_select(connection, query, [f"%{key_name}%"])

    def upd_element_in_column(self, table_name: str, set_upd_par_name: str, set_key_par_name: str, upd_column_name: str, key_column_name: str):
        with create_connection(self.DBNAME) as connection:
            query = f"UPDATE {table_name} SET {upd_column_name} = ? WHERE {key_column_name} = ?"
            execute_query(connection, query, [set_upd_par_name, set_key_par_name])
