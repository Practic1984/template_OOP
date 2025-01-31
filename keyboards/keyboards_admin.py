from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# def admin_menu_main():
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 5
#     lst = []
#     for i in range(1,90):

#         lst.append(
#         InlineKeyboardButton(i, callback_data=f"{i}")                                       
#     )
#     markup.add(*lst)
#     print('len keayboards ', len(lst))
#     return markup

def admin_menu_main():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Отчет по клиентам", callback_data="report_users"),
        InlineKeyboardButton("Отчет по рекламе", callback_data="report_utm"),
        InlineKeyboardButton("Рассылка", callback_data="push_msg"),                       
                     
    )

    return markup