
from bot_and_db import bot
from bot_and_db import db_users
import keyboards
import time
from msg import msg_admin
from keyboards import keyboards_admin
from config import config
from utils import other, admin_sql_query

def start_fnc_admin(message):
    # Обрабатывает команду /admin для администраторов
    if message.from_user.id in config.ADMIN_LIST:
        bot.send_message(chat_id=message.from_user.id, text=msg_admin.start_msg_admin, reply_markup=keyboards_admin.admin_menu_main())
                
    # Проверяет наличие таблицы администраторов и создаёт её, если отсутствует                
    if not db_users.check_table(table='admins'):
        db_users.create_table(create_query=admin_sql_query.create_table_admins)

    elif not db_users.check_user_on_table(table='admins', from_user_id=message.from_user.id):
        db_users.ins_unique_row(table_name='admins', values={
            'from_user_id': message.from_user.id,
            'from_user_username': message.from_user.username,
            'from_user_first_name': message.from_user.first_name,
            'regtime': other.get_time()
            })

def callback_query_report(call):

    # Обрабатывает нажатие на кнопку 'Отчёты' в админском меню
    file_path = db_users.get_full_db_report(message=call)
    with open(file_path, 'rb') as report_file:
        bot.send_document(chat_id=call.from_user.id, document=report_file, caption=msg_admin.msg_admin_report)


def callback_query_push(call):
    # Запрашивает у администратора сообщение для рассылки
    if call.from_user.id in config.ADMIN_LIST:
        m = bot.send_message(chat_id=call.from_user.id, text=msg_admin.msg_admin_push_msg)
        bot.register_next_step_handler(m, push_msg)
                

def push_msg(message):
    if message.from_user.id not in config.ADMIN_LIST:
        return
    
    # Запускаем рассылку в отдельном потоке
    # threading.Thread(target=send_broadcast, args=(message,)).start()
    
    bot.send_message(config.LOG_GROUP, "Рассылка началась. Статус будет в лог-группе.")
    try:
        users = db_users.get_all_users()
        
        print(users)
        total_users = len(users)
        success = 0
        failed = []
        start_time = time.time()
        
        # Первое сообщение в лог-группу
        log_msg = bot.send_message(config.LOG_GROUP, 
                                    f"📨 Рассылка начата\n"
                                    f"👥 Всего получателей: {total_users}\n"
                                    f"⏳ Статус: 0/{total_users} (0%)").message_id
        counter = 0
        for user_id in users:
            # user_id = 1029045407
            # user_id = user_row['from_user_id']
            try:
                print(user_id)
                
                # Пересылка оригинального сообщения

                bot.forward_message(chat_id=user_id, from_chat_id=message.from_user.id, message_id=message.message_id)
                success += 1
                
                # Обновляем статус каждые 20 отправок или 5% пользователей
                if (counter + 1) % max(20, total_users // 20) == 0:
                    progress = (counter + 1) / total_users * 100
                    bot.edit_message_text(
                        chat_id=config.LOG_GROUP,
                        message_id=log_msg,
                        text=f"📨 Рассылка в процессе\n"
                                f"👥 Всего получателей: {total_users}\n"
                                f"✅ Успешно: {success}\n"
                                f"❌ Ошибок: {len(failed)}\n"
                                f"⏳ Статус: {counter + 1}/{total_users} ({progress:.1f}%)"
                    )
                
                time.sleep(0.3)  # Защита от флуда
                
            except Exception as e:
                print(e)
                failed.append(user_id)
                time.sleep(1)
        
        # Финальный отчет
        duration = int(time.time() - start_time)
        bot.send_message(
            config.LOG_GROUP,
            f"✅ Рассылка завершена\n"
            f"⏱ Время: {duration} сек\n"
            f"👥 Всего: {total_users}\n"
            f"✅ Успешно: {success}\n"
            f"❌ Ошибок: {len(failed)}\n"
            f"💯 Успешных: {success/total_users*100:.1f}%\n\n"
            f"Список ошибок: {failed[:10]}{'...' if len(failed) > 10 else ''}"
        )
        
    except Exception as e:
        bot.send_message(config.LOG_GROUP, f"‼ Ошибка рассылки: {str(e)}")

    
def register_handler_admin(bot):
    # Регистрирует обработчики команд и callback-запросов для администраторов
    bot.register_message_handler(start_fnc_admin, commands=['admin'])
    bot.register_callback_query_handler(callback_query_report, func=lambda call: call.data.startswith('report'))
    bot.register_callback_query_handler(callback_query_push, func=lambda call: call.data.startswith('push_msg'))