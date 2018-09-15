#!/usr/bin/env python3.5
# encoding: utf-8
from email.mime.text import MIMEText
from functools import wraps
import hashlib
import logging
from uuid import uuid4

import aiosmtplib
from aiosmtplib.errors import SMTPTimeoutError


from config import EMAIL

COLORS = {
    'red': "\033[1;31m",
    'blue': "\033[1;34m",
    'yellow': "\033[1;33m",
    'green': "\033[0;32m",
    'other': "\033[1;35m",
    'grey': "\033[1;30m",
    'cyan': "\033[1;36m",
    'white': "\033[1;37m",
    'sred': "\033[1;38m",
}
COLOR_RESET = "\033[0;0m"


def color_print(*args, color='red', **kwargs):
    color = COLORS.get(color, COLORS.get('other'))
    print(color, *args, COLOR_RESET, **kwargs)


def get_args(args_dict):
    for arg, val in args_dict.items():
        if isinstance(val, list):
            args_dict[arg] = {
                'true': True,
                'True': True,
                'false': False,
                'False': False
            }.get(val[0], val[0])
    return args_dict


def safe_del_key(data, unwanted_key):
    """
    safe deleter of keys
    :param data: dict
    :param unwanted_key: str or list
    :return:
    """
    if isinstance(unwanted_key, str):
        if unwanted_key in data.keys():
            del data[unwanted_key]
    elif isinstance(unwanted_key, list):
        for ukey in unwanted_key:
            data = safe_del_key(data, ukey)
    return data


class SingletonDecorator:
    def __init__(self, a_class):
        self.a_class = a_class
        self.instance = None

    def __call__(self, *args, **kwargs):
        if not self.instance:
            self.instance = self.a_class(*args, **kwargs)
            self.instance.__wrapped__ = self
        return self.instance


def error_catcher(func, default_return=False):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            if args and hasattr(args[0], 'logger'):
                args[0].logger.exception(error)
            else:
                logging.exception(error)
            return default_return
    return wrapped


def hash_string(password):
    return hashlib.sha256(password.encode()).hexdigest()


async def send_email(recipients=None, subject='', text=''):
    if not isinstance(recipients, list):
        recipients = [recipients]
    try:
        server = aiosmtplib.SMTP(hostname=EMAIL.SERVER, port=EMAIL.PORT)
        await server.connect(timeout=5, use_tls=True)
        await server.login(username=EMAIL.USERNAME, password=EMAIL.PASSWORD)
        message = MIMEText(text)
        message['From'] = 'PyLove.org <{}>'.format(EMAIL.USERNAME)
        message['Subject'] = subject
        sender = EMAIL.USERNAME
        resp = await server.sendmail(sender, recipients, message.as_string(), timeout=10)
        return True
    except SMTPTimeoutError:
        logging.exception('error sending email')
        logging.error(EMAIL.SERVER)
    except:
        logging.exception('error sending email')
    return False


def create_uuid():
    return str(uuid4()).replace('-', '')


class ClassProperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
