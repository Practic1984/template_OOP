import datetime
import pytz
import re
from dateutil.relativedelta import relativedelta

def get_time(timezone: str = "Europe/Moscow") -> str:
    """
    Returns the current time for the specified timezone in "YYYY-MM-DD HH:MM" format.
    
    :param timezone: Timezone string in IANA format (e.g., "Europe/Moscow", "UTC", "Asia/Tokyo").
                     Defaults to "Europe/Moscow".
    :return: Current time as a string in "YYYY-MM-DD HH:MM" format.
    """
    try:
        tz = pytz.timezone(timezone)  # Get the timezone object
        current_time = datetime.now(tz)  # Get the current time
        return current_time.strftime('%Y-%m-%d %H:%M')  # Format without seconds and timezone info
    except pytz.UnknownTimeZoneError:
        raise ValueError(f"Invalid timezone: {timezone}")


# функция распарсивания deep-link ссылка бота
def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

def check_fio(fio_text: str) -> bool:
    """
    Checks whether the entered full name matches the "Full Name" format.
    Your full name must consist of 2 or 3 words, each with at least 2 letters
    """
    fio_text = fio_text.strip()
    lst_fio = fio_text.split()
    
    # Check the number of words and that each word consists of at least 2 letters
    return 2 <= len(lst_fio) <= 3 and all(len(word) >= 2 and re.fullmatch(r'[А-Яа-яЁё]+', word) for word in lst_fio)


def check_phone(phone_text_input: str) -> str | None:
    """
    Checks the entered phone number and converts it to a standard format.
    Returns a string with the number (e.g., "+79011234567") or None if the number is invalid.
    """
    phone_digits = "".join(re.findall(r'\d+', phone_text_input))  # Extract only digits

    if len(phone_digits) == 11:  # Check that the number consists of 11 digits
        return f"+{phone_digits}" if phone_text_input.strip().startswith("+7") else phone_digits

    return None


from datetime import datetime
from dateutil.relativedelta import relativedelta

def check_age(age_text: str) -> bool | None:
    """
    Checks if the entered birth date is valid and if the person is at least 18 years old.
    
    :param age_text: Birthdate in "DD.MM.YYYY" format.
    :return: True if the person is 18 or older, False if younger, None if the date is invalid or in the future.
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
    Validates an email address using a regular expression.
    
    :param email: The email address to validate.
    :return: True if the email is valid, otherwise False.
    """
    email = email.strip().lower()  # Remove spaces and convert to lowercase
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Email regex pattern
    
    return bool(re.match(pattern, email))  # Check if email matches the pattern

