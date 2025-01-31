# -*- coding: utf-8 -*-
#!/usr/bin/python3.12.3

from handlers import user
from handlers import admin
from bot_and_db import bot


print('Bot is Start')

def main():    
    # Регистрируем команды Пользователей
    user.register_handler_user(bot=bot)   

    # Регистрируем команды Админов   
    admin.register_handler_admin(bot=bot)   
   
    # Запускаем бесконечный цикл прослушивания новых сообщений
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    main()
     

    