# python3.12.3
"""
The script allows you to access the SQlite3 database 
through a function, which is more convenient than 
the syntax of direct SQL queries. For questions and 
comments, write to the author @Practic_old
"""
import sqlite3
import pandas as pd
import os
from sqlite3 import Error
import logging
from utils import user_sql_query
from utils import admin_sql_query
from config import config

from utils import other
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        logging.error(f"SQL error: {e}")
 
    return connection

def execute_query(connection, query, params=[]):
    """ 
    Function for recording
    to sql database
    connection : database connection
    query: str SQLite query string
    params: list request parameters
    """
    res = None
    cursor = connection.cursor()
    try:

        if len(params) > 0:

            cursor.execute(query, params)
            # res = cursor.fetchone() # fetchall()
        else:
            cursor.execute(query)
            res = cursor.fetchall()
        connection.commit()
        print("Query executed successfully")

    except Error as e:
        logging.error(f"Connection error: {e}")

    return res

def execute_query_select(connection, query, params=[]):
    """ 
    Function for reading from sql database
    returns a list of tuples
    connection : database connection
    query: str SQLite query string
    params: list request parameters
    """
    res = None
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        res = cursor.fetchall()

        connection.commit()
        print("Query executed successfully")
    except Error as e:
        logging.error(f"Connection error: {e}")

    return res

class SQLiteDB():

    def __init__(self, DBNAME):
        self.DBNAME = DBNAME
       
    def create_table_users(self, message):
        """
        create table users if not exist
        """
        with create_connection(self.DBNAME) as connection:
            execute_query(connection, user_sql_query.create_table_users)
            execute_query(connection, user_sql_query.save_user, [
                message.from_user.id, 
                message.from_user.username,
                message.from_user.first_name,
                other.get_msk_time()
            ])

    def create_table_admins(self, message):
        """
        create table admins if not exist
        """
        with create_connection(self.DBNAME) as connection:
            execute_query(connection, admin_sql_query.create_table_admins)
            execute_query(connection, admin_sql_query.save_admin, [
                message.from_user.id, 
                message.from_user.username,
                message.from_user.first_name,
                other.get_msk_time()
            ])
        

    def create_table_utm(self):
        """
        create table utm if not exist
        """

        with create_connection(self.DBNAME) as connection:
            execute_query(connection, user_sql_query.create_table_utm)

            connection = create_connection(self.DBNAME)
            query = user_sql_query.create_table_utm
            execute_query(connection=connection, query=query, params=[])
        
    def check_table(self, table: str):
        """
        Check table name is exists in database
        """
        connection = create_connection(self.DBNAME)
        cursor = connection.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
        res = cursor.fetchone()
        connection.close()
        if res: return True
        else:
            return False
        
    def check_user_on_table(self, table: str, from_user_id: int):
        """
        Check user on table by from_user_id
        """
        connection = create_connection(self.DBNAME)
        cursor = connection.cursor()
        cursor.execute(f"SELECT from_user_id FROM {table} WHERE from_user_id=?;", (from_user_id,))
        res = cursor.fetchone()
        connection.close()
        if res: 
            return True
        else:
            return False    
        

    def get_user_row(self, from_user_id: int):
        """
        Function for reading from sql database
        returns a dictionary of tuples
        connection : database connection
        from_user_id : int
        """
        with create_connection(self.DBNAME) as connection:
            connection.row_factory = sqlite3.Row  
            cursor = connection.cursor()
            cursor.execute(user_sql_query.get_user_row, [from_user_id])
            row = cursor.fetchone()
            return dict(row) if row else None


    def get_admin_row(self, from_user_id: int ):
        """
        Function for reading from sql database
        returns a dictionary of tuples
        connection : database connection
        from_user_id : int
        """
        with create_connection(self.DBNAME) as connection:
            connection.row_factory = sqlite3.Row  
            cursor = connection.cursor()
            cursor.execute(admin_sql_query.get_admin_row, [from_user_id])
            row = cursor.fetchone()
            return dict(row) if row else None


    def get_table_report( self, message, table):
        connection = create_connection(self.DBNAME)
        query = admin_sql_query.get_table_rows.format(table=table)
        all_records = pd.read_sql_query(query, connection)
        len_of_records = len(all_records) if not all_records.empty else 0
        os.makedirs("./reports", exist_ok=True) 
        path = f'./reports/report_{table}_{message.from_user.id}.xlsx'       
        all_records.to_excel(path, index=False)
        connection.close()
        
        return path, len_of_records           

    def get_all_users(self) -> list:
        """
        Получает всех пользователей и возвращает список user_id.
        """
        query = admin_sql_query.get_all_users

        with create_connection(self.DBNAME) as connection:
            all_records_users = pd.read_sql_query(query, connection)

        # Проверяем, есть ли колонка 'from_user_id', иначе возвращаем пустой список
        if 'from_user_id' not in all_records_users.columns or all_records_users.empty:
            return []

        return all_records_users['from_user_id'].astype(int).tolist()
    
    def find_table_or_column(self, table_name: str, column_name: str) -> list[dict]:
        """
        Ищет все значения по указанным колонкам в таблице.
        :param table_name: str - название таблицы
        :param column_name: str - название колонки или несколько колонок через запятую
        :return: list[dict] - список словарей с данными
        """
        if table_name not in config.ALLOWED_TABLES:
            raise ValueError(f"Недопустимое название таблицы: {table_name}")

        # Проверяем, что column_name содержит только разрешённые символы (буквы, цифры, запятая)
        if not all(part.isidentifier() or part == '*' for part in column_name.replace(" ", "").split(",")):
            raise ValueError("Недопустимое название колонки")

        query = f"SELECT {column_name} FROM {table_name}"

        with create_connection(self.DBNAME) as connection:
            connection.row_factory = sqlite3.Row  # Позволяет получать результаты как словари
            result = execute_query_select(connection, query=query, params=[])

        return [dict(row) for row in result] if result else []
    

    def find_elements_in_column(self, table_name: str, column_name: str, key_name: str) -> list[dict]:
        """
        Ищет записи по значению в указанной колонке.
        :param table_name: str - имя таблицы
        :param key_name: str - значение для поиска
        :param column_name: str - имя колонки
        :return: list[dict] - список найденных строк
        """
        if table_name not in config.ALLOWED_TABLES:
            raise ValueError(f"Недопустимое название таблицы: {table_name}")

        if not column_name.isidentifier():  # Проверка на корректность названия колонки
            raise ValueError("Недопустимое название колонки")

        query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"

        with create_connection(self.DBNAME) as connection:
            connection.row_factory = sqlite3.Row  # Позволяет получать результаты как dict
            result = execute_query_select(connection, query=query, params=[key_name])

        return [dict(row) for row in result] if result else []
    

    def find_elements_by_keyword(self, table_name: str, key_name: str, column_name: str) -> list[dict]:
        """
        Ищет записи, содержащие `key_name` в колонке `column_name`.
        :param table_name: str - имя таблицы
        :param key_name: str - строка для поиска
        :param column_name: str - имя колонки
        :return: list[dict] - список найденных строк
        """
        if table_name not in config.ALLOWED_TABLES:
            raise ValueError(f"Недопустимое название таблицы: {table_name}")

        if not column_name.isidentifier():  # Проверка на корректность названия колонки
            raise ValueError("Недопустимое название колонки")

        query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?"
        params = [f"%{key_name}%"]

        with create_connection(self.DBNAME) as connection:
            connection.row_factory = sqlite3.Row  # Позволяет получать результаты как dict
            result = execute_query_select(connection, query=query, params=params)

        return [dict(row) for row in result] if result else []
    
    
    def upd_element_in_column(self, table_name: str, upd_column_name: str, new_value: str, key_column_name: str, key_value: str):
        """
        Обновляет данные в таблице.
        :param table_name: str - название таблицы
        :param upd_column_name: str - колонка, которую обновляем
        :param new_value: str - новое значение для установки
        :param key_column_name: str - колонка, по которой ищем
        :param key_value: str - значение для поиска
        """
        if table_name not in config.ALLOWED_TABLES:
            raise ValueError(f"Недопустимое название таблицы: {table_name}")

        if not (upd_column_name.isidentifier() and key_column_name.isidentifier()):
            raise ValueError("Недопустимое название колонки")

        query = f"""
            UPDATE {table_name}
            SET {upd_column_name} = ?
            WHERE {key_column_name} = ?
        """

        with create_connection(self.DBNAME) as connection:
            execute_query(connection, query=query, params=[new_value, key_value])

    
    def delete_table(self, table):
            """
            ERASE table
            DELETE all rows from table
            """
            connection = create_connection(self.DBNAME)
            query = f"""
            DELETE FROM "{table}"
                    """ 
            execute_query(connection, query=query, params=[])
            connection.close() 

    def delete_row(self, table:str, key_name:str, column_name:str):
            """
            DELETE rows from table by key 
            """
            connection = create_connection(self.DBNAME)
            query = f"""
            DELETE FROM "{table}"
            WHERE {column_name} = ?
                    """ 
            execute_query(connection, query=query, params=[key_name])
            connection.close() 


