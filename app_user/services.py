import imghdr
import re


def check_password(password):
    if len(password) < 8:
        return 'Длина пароль должна быть больше 8 символов', False
    elif re.search(r'[0-9]', password) is None:
        return 'Пароль должен содержать минимум 1 цифру', False
    elif re.search(r'[A-Z]|[А-Я]', password) is None:
        return 'Пароль должен содержать минимум 1 символ в верхем регистре', False
    else:
        return 'Ок', True


def is_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return False
    return '.' + (format if format != 'jpeg' else 'jpg')
