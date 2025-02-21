
from bot_and_db import bot
from bot_and_db import db_users
import keyboards
import time
from msg import msg_admin
from keyboards import keyboards_admin
from config import config


def start_fnc_admin(message):
    # Обрабатывает команду /admin для администраторов
    if message.from_user.id in config.ADMIN_LIST:
        bot.send_message(chat_id=message.from_user.id, text=msg_admin.start_msg_admin, reply_markup=keyboards_admin.admin_menu_main())
                
    # Проверяет наличие таблицы администраторов и создаёт её, если отсутствует                
    if not db_users.check_table(table='admins'):
        db_users.create_table_admins(message=message)

    elif not db_users.check_user_on_table(table='admins', from_user_id=message.from_user.id):
        db_users.create_table_admins(message=message)


def callback_query_report_users(call):
    # Генерирует отчёт по пользователям и отправляет администратору
    if call.from_user.id in config.ADMIN_LIST:
        path, len_of_records = db_users.get_table_report(message=call, table='users')
        with open(path, mode='rb') as report_file:
            bot.send_document(call.from_user.id, document=report_file, caption=msg_admin.msg_admin_report_users.format(len_of_records=len_of_records))

def callback_query_report_utm(call):
    # Генерирует отчёт по UTM-меткам и отправляет администратору
    if call.from_user.id in config.ADMIN_LIST:
        path, len_of_records = db_users.get_table_report(message=call, table='utm')
        with open(path, mode='rb') as report_file:
            bot.send_document(call.from_user.id, document=report_file, caption=msg_admin.msg_admin_report_utm.format(len_of_records=len_of_records))

def callback_query_push(call):
    # Запрашивает у администратора сообщение для рассылки
    if call.from_user.id in config.ADMIN_LIST:
        m = bot.send_message(chat_id=call.from_user.id, text=msg_admin.msg_admin_push_msg)
        bot.register_next_step_handler(m, get_push_msg)
                
def get_push_msg(message):
    # Получает сообщение для рассылки и отправляет его всем пользователям
    if message.from_user.id in config.ADMIN_LIST:
        msg = message.text
        list_of_users = db_users.get_all_users()  
        print(list_of_users)
        count_push = 0
        for user_id in list_of_users:
            try:
                print(message)
                bot.forward_message(chat_id=user_id, from_chat_id=message.from_user.id, message_id=message.message_id)          
                count_push += 1
                if count_push % 15 == 0:
                    bot.send_message(chat_id=message.from_user.id, text=f"Доставлено {count_push} шт.")

                
            except Exception as ex:                   
                    bot.send_message(chat_id=message.from_user.id, text=f"{user_id} failed")
                    #здесь юзера удаляем из базы кто бота заблочил
                    db_users.delete_row(table='users', key_name=user_id, column_name='from_user_id')
                    
                    time.sleep(1)
            bot.send_message(chat_id=message.from_user.id, text=f"Рассылка закончена отправлено {count_push}")
    
def register_handler_admin(bot):
    # Регистрирует обработчики команд и callback-запросов для администраторов
    bot.register_message_handler(start_fnc_admin, commands=['admin'])
    bot.register_callback_query_handler(callback_query_report_users, func=lambda call: call.data.startswith('report_users'))
    bot.register_callback_query_handler(callback_query_report_utm, func=lambda call: call.data.startswith('report_utm'))
    bot.register_callback_query_handler(callback_query_push, func=lambda call: call.data.startswith('push_msg'))