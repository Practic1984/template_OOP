
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
