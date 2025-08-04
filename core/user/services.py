from random import randint
from django.utils import timezone
from datetime import timedelta

def generate_otp():
    otp = randint(100000,999999)
    return otp


def is_code_valid(verification_code_instance):
    now = timezone.now()
    expiration_time = verification_code_instance.created_date + timedelta(minutes=2)
    return now <= expiration_time