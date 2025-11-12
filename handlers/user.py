
from bot_and_db import bot
from bot_and_db import db_users
import utils
from utils import other, user_sql_query
from msg import msg_user
from keyboards import keyboards_user

def start_fnc_user(message):
    """
    Обработчик команды /start.
    Проверяет, существует ли таблица users, если нет — создаёт её и записывает пользователя.
    Если таблица есть, но пользователя в ней нет, также добавляет его.
    """

    # Создаем таблицу users, если её нет, и записываем туда пользователя
    if not db_users.check_table(table='users'):
        db_users.create_table(create_query=user_sql_query.create_table_users)
    
    if not db_users.check_user_on_table(table='users', from_user_id=message.from_user.id):
        db_users.ins_unique_row(table_name='users', values={
            'from_user_id': message.from_user.id,
            'from_user_username': message.from_user.username,
            'from_user_first_name': message.from_user.first_name,
            'regtime': other.get_time()            
            })
        
            
    unique_code = other.extract_unique_code(message.text)
    if not db_users.check_table(table='utm'):
        db_users.create_table(create_query=user_sql_query.create_table_utm)

    # Получаем уникальный код из команды /start
    if unique_code:  # if the '/start' command contains a unique_code

        #создаем таблицу utm если ее нет и записываем туда юзера с utm меткой
        db_users.ins_unique_row(table_name='utm', values={
            'from_user_id': message.from_user.id,
            'from_user_username': message.from_user.username,
            'from_user_first_name': message.from_user.first_name,
            'regtime': other.get_time(),
            'utm_code': unique_code
            })
        
    bot.send_message(chat_id=message.from_user.id, text=msg_user.start_msg_user, reply_markup=keyboards_user.user_menu_main())


def callback_query_about(call):
    """
    Обработчик нажатия на кнопку 'О нас'.
    Обновляет время просмотра раздела "О нас" в базе данных.
    Отправляет пользователю сообщение с информацией.
    """
    db_users.upd_element_by_filters(table_name="users", upd_column_name="about_time", new_value=other.get_time(), filters={ 'from_user_id': call.from_user.id })
    bot.send_message(chat_id=call.from_user.id, text=msg_user.about_msg, reply_markup=keyboards_user.back())


def callback_query_faq(call):
    """
    Обработчик нажатия на кнопку 'FAQ'.
    Обновляет время просмотра раздела "FAQ" в базе данных.
    Отправляет пользователю сообщение с часто задаваемыми вопросами.
    """
    db_users.upd_element_by_filters(table_name="users", upd_column_name="faq_time", new_value=other.get_time(), filters={ 'from_user_id': call.from_user.id })
    bot.send_message(chat_id=call.from_user.id, text=msg_user.faq_msg, reply_markup=keyboards_user.back())
                            
def callback_query_back(call):
    """
    Обработчик нажатия на кнопку 'Назад'.
    Возвращает пользователя в главное меню.
    """
    bot.send_message(chat_id=call.from_user.id, text=msg_user.start_msg_user,reply_markup=keyboards_user.user_menu_main())

def register_handler_user(bot):
    """
    Регистрация обработчиков команд и callback-запросов для пользователя.
    """
    bot.register_message_handler(start_fnc_user, commands=['start']) 
    bot.register_callback_query_handler(callback_query_about, func=lambda call: call.data.startswith('about'))
    bot.register_callback_query_handler(callback_query_faq, func=lambda call: call.data.startswith('faq'))
    bot.register_callback_query_handler(callback_query_back, func=lambda call: call.data.startswith('back'))

