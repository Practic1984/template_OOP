import re
from datetime import datetime
import pytz

def validate_email(email: str) -> bool:
    """
    Validates an email address using a regular expression.
    
    :param email: The email address to validate.
    :return: True if the email is valid, otherwise False.
    """
    email = email.strip().lower()  # Remove spaces and convert to lowercase
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Email regex pattern
    
    return bool(re.match(pattern, email))  # Check if email matches the pattern

print(validate_email(email='vasya@mailru'))