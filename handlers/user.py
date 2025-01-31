
from bot_and_db import bot
from bot_and_db import db_users
import utils
from msg import msg_user
from keyboards import keyboards_user

def start_fnc_user(message):
    # команда /start
    
    #создаем таблицу users если ее нет и записываем туда юзера
    if not db_users.check_table(table='users'):
        db_users.create_table_users(message=message)
    
    elif not db_users.check_user_on_table(table='users', from_user_id=message.from_user.id):
        db_users.create_table_users(message=message)
        
            
    unique_code = utils.other.extract_unique_code(message.text)

    if unique_code:  # if the '/start' command contains a unique_code

        #создаем таблицу utm если ее нет и записываем туда юзера с utm меткой
        db_users.create_table_utm(message=message, unique_code=unique_code)     
    
    bot.send_message(chat_id=message.from_user.id, text=msg_user.start_msg_user, reply_markup=keyboards_user.user_menu_main())

def callback_query_about(call):
    # calldata about
    db_users.upd_element_in_column(table_name='users', set_upd_par_name='about_time', set_key_par_name=utils.other.get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
    bot.send_message(chat_id=call.from_user.id, text=msg_user.about_msg, reply_markup=keyboards_user.back())

def callback_query_faq(call):
    # calldata faq
    db_users.upd_element_in_column(table_name='users', set_upd_par_name='faq_time', set_key_par_name=utils.other.get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
    bot.send_message(chat_id=call.from_user.id, text=msg_user.faq_msg, reply_markup=keyboards_user.back())
                            
def callback_query_back(call):
    #calldata back
    bot.send_message(chat_id=call.from_user.id, text=msg_user.start_msg_user,reply_markup=keyboards_user.user_menu_main())

def register_handler_user(bot):
    bot.register_message_handler(start_fnc_user, commands=['start']) 
    bot.register_callback_query_handler(callback_query_about, func=lambda call: call.data.startswith('about'))
    bot.register_callback_query_handler(callback_query_faq, func=lambda call: call.data.startswith('faq'))
    bot.register_callback_query_handler(callback_query_back, func=lambda call: call.data.startswith('back'))

