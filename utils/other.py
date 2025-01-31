import datetime
import pytz

def get_msk_time() -> datetime:
    """
    Функция получения текущего времени в Москве
    """
    time_now = datetime.datetime.now(pytz.timezone("Europe/Moscow"))
    time_now = time_now.strftime('%Y-%m-%d %H:%M:%S')
    return time_now


# функция распарсивания deep-link ссылка бота
def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

def check_fio(fio_text):
    """
    Функция проверки введенного ФИО текстом, 
    возвращает True, если формат Ф И О, 
    либо возвращает False
    """
    fio_text = fio_text.strip()
    if len(fio_text.split(' ')) <= 3:
        if len(fio_text.split(' ')) > 1:
            lst_fio = fio_text.split(' ')
            for i in lst_fio:
                if len(i) < 2:
                    return False
            return True
        
    else:
        return False


def check_phone(phone_text_input):
    """
    Функция проверки введенного телефона текстом, 
    вытаскивает цифры, либо возвращает None
    """
    phone_text = re.findall(r'\d+', phone_text_input)
    print(phone_text)
    valid_phone_text = ''

    if len(phone_text) == 1:
        valid_phone_text = phone_text[0]

    elif len(phone_text) > 1:
        text = ''
        for i in phone_text:
            valid_phone_text += i

    else:
        valid_phone_text = None
        
    try:
        if len(valid_phone_text) == 11:
            print(phone_text_input.strip())
            if '+7' in phone_text_input:
                return f"+{valid_phone_text}"
            else:
                return valid_phone_text
        else:
            return None
    except Exception as e:
        return None


def check_age(age_text):
    """
    Функция проверки введенного возраста текстом, 
    возвращает True, если формат 10.12.2010, 
    либо возвращает None
    """
    age_text = age_text.strip()
    try:
        if len(age_text.split('.')) == 3:
            date_age = datetime.datetime.strptime(age_text, '%d.%m.%Y').date()
            date_now = datetime.datetime.now().date()
            delta_date = date_now - date_age
            vozrast = delta_date.days/365.2425
            if vozrast >= 18:
                return 'True'
            elif vozrast <=0:
                return 'god_ne_nastupil'
            elif vozrast < 18:
                return 'False'
        else:
            return 'None'
    except Exception as ex:
        return 'None'
