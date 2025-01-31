import sqlite3
import json

from config import config
import telebot
from utils.sqliteormmagic import SQLiteDB

# Создаем обьект бота
bot = telebot.TeleBot(config.TOKEN)
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "Перезапуск бота"),
    ],)
db_users = SQLiteDB('./utils/users.db')

# res = db_users.check_table(table='user')
# res = db_users.check_user_on_table(table='users', from_user_id=1029045407)
res = db_users.find_elements_in_column(table_name='users', column_name='from_user_id', key_name=1029045407)
print(res)
