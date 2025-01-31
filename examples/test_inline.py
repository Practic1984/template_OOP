# -*- coding: utf-8 -*-
import telebot
from telebot import types, logger
from telebot.types import  InputMediaPhoto, InputMediaVideo, InputMediaDocument
import pandas as pd
# 04_01_2025
import sys
import logging
import msg
import os
import keybords
import time
import utils
from sqliteormmagic import SQLiteDB
import sqliteormmagic as som


from config import TOKEN, ADMIN_LIST

bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML', skip_pending=True)    
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "Запуск бота"),
        telebot.types.BotCommand("luck", "Испытать удачу"),       
        telebot.types.BotCommand("balance", "Мой баланс"),   
        telebot.types.BotCommand("help", "Правила"),                     
    ],)

db_users = SQLiteDB('users.db')


def main():
    @bot.message_handler(commands=['start'])
    def start_fnc(message):
        utils.cr_table_users(message)
        db_users.create_table('reklama', [
        ("from_user_id", 'INTEGER'), 
        ("from_user_username", 'TEXT'), 
        ("reg_time", 'TEXT'),       
        ("utm_code", 'TEXT'),                         
        ])
        unique_code = utils.extract_unique_code(message.text)
        print(unique_code)

        if unique_code:  # if the '/start' command contains a unique_code
            db_users.ins_unique_row('reklama', [
            ("from_user_id", message.from_user.id), 
            ("from_user_username", message.from_user.username), 
            ("reg_time", utils.get_msk_time()),         
            ("utm_code", unique_code),    
            ])  
    
        bot.send_message(chat_id=message.from_user.id, text=msg.start_msg_user,reply_markup=keybords.user_menu_main())
    
    @bot.message_handler(commands=['balance'])
    def balance_fnc(message):          
        balance = utils.db_users.find_one_value_from_row(value='balance', table_name='balance', column_name='from_user_id', key_name=message.from_user.id)
        text = f"""
Мой баланс: {balance} бал.

Чтобы ознакомиться с правилами обмена и начисления баллов нажмите /help
"""
        bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=keybords.change_board())

    @bot.message_handler(commands=['luck'])
    def dice_fnc(message):            

        m = bot.send_dice(chat_id=message.from_user.id, emoji="⚽")
        dice_result = m.dice.value
        time.sleep(4)
        utils.cr_table_balance(message=message)
        balance = utils.db_users.find_one_value_from_row(value='balance', table_name='balance', column_name='from_user_id', key_name=message.from_user.id)
        
        if dice_result in [4]:
            bot.send_message(chat_id=message.from_user.id, text="🔥 Красивый гол +2 балла! 🔥")
            balance += 2

        elif dice_result in [3]:
            bot.send_message(chat_id=message.from_user.id, text="🔥 Вы можете лучше +1 балл! 🔥")           
            balance += 1

        elif dice_result in [2]:
            bot.send_message(chat_id=message.from_user.id, text="🔥 Так себе удар -1 балл! 🔥")           
            balance -= 1            
    
        elif dice_result in [1]:
            bot.send_message(chat_id=message.from_user.id, text="🔥 Вы серьезно? -1 балл! 🔥")           
            balance -= 1

        elif dice_result in [5]:
            bot.send_message(chat_id=message.from_user.id, text="🔥 Вполне неплохо! +1 балл! 🔥")           
            balance += 1

        if balance < 0:
            balance = 0

        bot.send_message(chat_id=message.from_user.id, text=f"Ваш баланс 👉 {balance}\nЧтобы ознкомиться с правилами нажмите /help")           
        db_users.upd_element_in_column(table_name='balance', set_upd_par_name='balance', set_key_par_name=balance, upd_column_name='from_user_id', key_column_name=message.from_user.id)
    
    
    @bot.message_handler(commands=['help'])
    def help_fnc(message):
        bot.send_message(chat_id=message.from_user.id, text=msg.msg_dice_start)       

    @bot.message_handler(commands=['admin'])
    def start_fnc(message):
        if message.from_user.id in ADMIN_LIST:
            bot.send_message(chat_id=message.from_user.id, text=msg.start_msg_admin, reply_markup=keybords.admin_menu_main())


    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        # клиентская часть
        if call.data == 'about':
            db_users.upd_element_in_column(table_name='users', set_upd_par_name='about_time', set_key_par_name=utils.get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.about_msg, reply_markup=keybords.back())

        elif call.data == 'change':
            pass







































































































































































































































































































































































































































































































































































































































        

        elif call.data == 'faq':
            db_users.upd_element_in_column(table_name='users', set_upd_par_name='faq_time', set_key_par_name=utils.get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.faq_msg, reply_markup=keybords.back())
                              

        elif call.data == 'contacts':
            db_users.upd_element_in_column(table_name='users', set_upd_par_name='contacts_time', set_key_par_name=utils.get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.contacts_msg, reply_markup=keybords.back())  

        elif call.data == 'back':
            bot.send_message(chat_id=call.from_user.id, text=msg.start_msg_user,reply_markup=keybords.user_menu_main())

        # админская часть
        elif call.data == 'report_utm':
            if call.from_user.id in ADMIN_LIST:
                connection = som.create_connection('users.db')
                query = f"""
                SELECT * FROM reklama 
                """
                all_records = pd.read_sql_query(query, connection)
                len_of_records = len(all_records['from_user_id'])
                all_records.to_excel('report.xlsx', index=False)
                connection.close()
                with open('report.xlsx', mode='rb') as filename:
                    bot.send_document(call.from_user.id, document=filename, caption=f'Всего {len_of_records} переходов. Отчет по статистике переходов по ссылкам в прикрепленном файле')
        
        elif call.data == 'report_users':
            if call.from_user.id in ADMIN_LIST:
                connection = som.create_connection('users.db')
                query = f"""
                SELECT * FROM users 
                """
                all_records = pd.read_sql_query(query, connection)
                len_of_records = len(all_records['from_user_id'])
                all_records.to_excel('report.xlsx', index=False)
                connection.close()
                with open('report.xlsx', mode='rb') as filename:
                    bot.send_document(call.from_user.id, document=filename, caption=f'Всего {len_of_records} переходов. Отчет по статистике пользователей в прикрепленном файле')

    
    bot.infinity_polling()

if __name__ == "__main__":
    main()

    