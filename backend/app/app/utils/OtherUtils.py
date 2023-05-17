import datetime
import random
import re


def email_validate(email: str):
    pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    return re.match(pattern, email) is not None


def generate_code(length: int = 5):
    return ''.join(random.choice('0123456789') for _ in range(length))


#TODO: вместо datetime хранить и обрабатывать timestamp
def generate_expired_in(live_ex: int = 10):
    return datetime.datetime.now() + datetime.timedelta(minutes=live_ex)
