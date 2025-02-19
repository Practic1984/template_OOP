# -*- coding: utf-8 -*-
#!/usr/bin/python3.12.3
"""
main file to run the project
"""

from handlers import user
from handlers import admin
from bot_and_db import bot


print('Bot is Start')

def main():    
    # Registering User teams
    user.register_handler_user(bot=bot)   

    # Registering Admin Teams
    admin.register_handler_admin(bot=bot)   
   
    # We start an endless loop of listening to new messages
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    main()
     

    