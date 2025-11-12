import datetime
import pytz
import re
from dateutil.relativedelta import relativedelta
from telebot.types import Message, CallbackQuery

def get_file_id(update):
    """
    Простая функция для получения file_id
    Возвращает только file_id или None
    """
    if isinstance(update, CallbackQuery):
        message = update.message
    elif isinstance(update, Message):
        message = update
    else:
        return None
    
    # Проверяем все типы медиа
    media_types = [
        message.voice,
        message.audio, 
        message.document,
        message.video,
        message.photo,
        message.sticker,
        message.video_note
    ]
    
    for media in media_types:
        if media:
            if media == message.photo:
                # Для фото берем самый большой размер
                return max(media, key=lambda p: p.file_size).file_id
            return media.file_id
    
    return None


def get_time(timezone: str = "Europe/Moscow") -> str:
    """
    Возвращает текущее время для указанного часового пояса в формате "YYYY-MM-DD HH:MM".
    
    :param timezone: Часовой пояс в формате IANA (например, "Europe/Moscow", "UTC", "Asia/Tokyo").
                     По умолчанию "Europe/Moscow".
    :return: Текущее время в виде строки в формате "YYYY-MM-DD HH:MM".
    """
    try:
        tz = pytz.timezone(timezone)  # Get the timezone object
        current_time = datetime.now(tz)  # Get the current time
        return current_time.strftime('%Y-%m-%d %H:%M')  # Format without seconds and timezone info
    except pytz.UnknownTimeZoneError:
        raise ValueError(f"Invalid timezone: {timezone}")


# функция распарсивания deep-link ссылка бота
def extract_unique_code(text):
    """
    Функция для извлечения уникального кода из команды /start.
    """
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

def check_fio(fio_text: str) -> bool:
    """
    Проверяет, соответствует ли введенное ФИО формату "Фамилия Имя" или "Фамилия Имя Отчество".
    ФИО должно состоять из 2 или 3 слов, каждое не менее 2 букв.
    """
    fio_text = fio_text.strip()
    lst_fio = fio_text.split()
    
    # Check the number of words and that each word consists of at least 2 letters
    return 2 <= len(lst_fio) <= 3 and all(len(word) >= 2 and re.fullmatch(r'[А-Яа-яЁё]+', word) for word in lst_fio)


def check_phone(phone_text_input: str) -> str | None:
    """
    Проверяет введенный номер телефона и преобразует его в стандартный формат.
    Возвращает строку с номером (например, "+79011234567") или None, если номер недействителен.
    """
    phone_digits = "".join(re.findall(r'\d+', phone_text_input))  # Extract only digits

    if len(phone_digits) == 11:  # Check that the number consists of 11 digits
        return f"+{phone_digits}" if phone_text_input.strip().startswith("+7") else phone_digits

    return None


from datetime import datetime
from dateutil.relativedelta import relativedelta

def check_age(age_text: str) -> bool | None:
    """
    Проверяет, корректна ли введенная дата рождения и исполнилось ли пользователю 18 лет.
    
    :param age_text: Дата рождения в формате "DD.MM.YYYY".
    :return: True, если пользователю 18 лет или больше, False, если меньше, None, если дата некорректна или в будущем.
    """
    try:
        birth_date = datetime.strptime(age_text.strip(), '%d.%m.%Y').date()  # Parse birthdate
        today = datetime.now().date()  # Get today's date
        
        if birth_date > today:
            return None  # Birthdate is in the future
        
        age = relativedelta(today, birth_date).years  # Calculate age
        
        return age >= 18  # Return True if 18 or older, False otherwise
    
    except ValueError:
        return None  # Return None if the date format is incorrect

def validate_email(email: str) -> bool:
    """
    Проверяет корректность email-адреса с использованием регулярного выражения.
    
    :param email: Email-адрес для проверки.
    :return: True, если email корректен, иначе False.
    """
    email = email.strip().lower()  # Remove spaces and convert to lowercase
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Email regex pattern
    
    return bool(re.match(pattern, email))  # Check if email matches the pattern

