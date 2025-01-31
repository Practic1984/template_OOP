from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import config
def user_menu_main():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("О проекте", callback_data="about"),
        InlineKeyboardButton("Faq", callback_data="faq"),
        InlineKeyboardButton("Отзывы", url=config.REVIEW_TG_URL),                           
        InlineKeyboardButton("Помощь", url=config.HELP_TG_URL),                         
    )

    return markup

def menu_main():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("В главное меню", callback_data="back"),
    )

    return markup

def change_board():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Обменять", callback_data="change"),
        InlineKeyboardButton("В главное меню", callback_data="back"),
    )

    return markup

def back():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Назад", callback_data="back"),
    )

    return markup

