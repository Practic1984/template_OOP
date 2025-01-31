# -*- coding: utf-8 -*-
import telebot
from telebot import types, logger
from telebot.types import  InputMediaPhoto, InputMediaVideo, InputMediaDocument
import pandas as pd

import sys
import logging
import msg
import os
import keybords

import utils
from sqliteormmagic import SQLiteDB
import sqliteormmagic as som


from config import TOKEN, ADMIN_LIST

bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML', skip_pending=True)    
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "Запуск бота"),
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
    
    @bot.message_handler(commands=['admin'])
    def start_fnc(message):
        if message.from_user.id in ADMIN_LIST:
            bot.send_message(chat_id=message.from_user.id, text=msg.start_msg_admin, reply_markup=keybords.admin_menu_main())

    @bot.message_handler(content_types=['photo'])
    def get_photo(message):
        foto = message.photo[len(message.photo) - 1].file_id
        file_info = bot.get_file(foto)
        photo = bot.download_file(file_info.file_path)
        msg = bot.save_photo()

    @bot.message_handler(content_types=['voice'])
    def get_photo(message):
        print(message)
        voice = message.voice.file_id
        file_info = bot.get_file(voice)
        voice = bot.download_file(file_info.file_path)
        db_users.upd_element_in_column(table_name='users', set_upd_par_name='voice', set_key_par_name=voice, upd_column_name='from_user_id', key_column_name=message.from_user.id)
        voice_bd = utils.get_value(value_name='voice', user_id=message.from_user.id)
        text = """
USER ID
USERNAME
"""
        bot.send_voice(chat_id=message.from_user.id, voice=voice_bd, caption=text)

    @bot.message_handler(content_types=['text'])
    def get_text(message):
        print(message)
        text = message.text
      
        db_users.upd_element_in_column(table_name='users', set_upd_par_name='voice', set_key_par_name=text, upd_column_name='from_user_id', key_column_name=message.from_user.id)
        text_bd = utils.get_value(value_name='voice', user_id=message.from_user.id)
        text = f"""
USER ID
USERNAME
ТЕКСТ: {text_bd}
"""
        bot.send_message(chat_id=message.from_user.id, text=text)        
        


    @bot.message_handler(content_types=['location'])
    def get_text(message):
        print(message)
        longitude = message.location.longitude
        latitude = message.location.latitude
        
#         bot.send_location()
#         db_users.upd_element_in_column(table_name='users', set_upd_par_name='voice', set_key_par_name=text, upd_column_name='from_user_id', key_column_name=message.from_user.id)
#         text_bd = utils.get_value(value_name='voice', user_id=message.from_user.id)
#         text = f"""
# USER ID
# USERNAME
# ТЕКСТ: {text_bd}
# """
        bot.send_location(chat_id=message.from_user.id, longitude=longitude, latitude=latitude)    

    @bot.message_handler(content_types=['contact'])
    def get_text(message):
        print(message)
        phone_number = message.contact.phone_number
        first_name = message.contact.first_name
        user_id = message.contact.user_id
        bot.send_contact(chat_id=message.from_user.id, phone_number=phone_number, first_name=first_name)
  
# 
        
#         bot.send_location()
#         db_users.upd_element_in_column(table_name='users', set_upd_par_name='voice', set_key_par_name=text, upd_column_name='from_user_id', key_column_name=message.from_user.id)
#         text_bd = utils.get_value(value_name='voice', user_id=message.from_user.id)
#         text = f"""
# USER ID
# USERNAME
# ТЕКСТ: {text_bd}
# """
   
    @bot.message_handler(content_types=['sticker'])
    def get_photo(message):
        print(message)
        sticker = message.sticker.file_id
        file_info = bot.get_file(sticker)
        sticker = bot.download_file(file_info.file_path)
        db_users.upd_element_in_column(table_name='users', set_upd_par_name='sticker', set_key_par_name=sticker, upd_column_name='from_user_id', key_column_name=message.from_user.id)
        sticker_bd = utils.get_value(value_name='sticker', user_id=message.from_user.id)
        text = """
USER ID
USERNAME
"""
        bot.send_sticker(chat_id=message.from_user.id, voice=sticker_bd, caption=text)

    bot.infinity_polling()

if __name__ == "__main__":
    main()

    