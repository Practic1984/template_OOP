from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu_main():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Отчеты", callback_data="report"),
        InlineKeyboardButton("Рассылка", callback_data="push_msg"),                       
                     
    )

    return markup