import random
from datetime import datetime, timedelta

import requests
from django.conf import settings

from .exceptions import BadRequestException


def send_otp(otp):
    message = f"""
    Project: CHESS-TURNER
    Phone_number: {otp.user.username}
    OTP_Code: {otp.otp_code}
    OTP_Key: {otp.otp_key}
    Expire_date: {otp.created_at + timedelta(minutes=3)}
    """
    status = requests.get(settings.TELEGRAM_API_URL.format(settings.BOT_TOKEN, message, settings.CHANNEL_ID))
    if status.status_code != 200:
        raise BadRequestException('The code could not be sent due to technical reasons! Please try again later.')


def generate_otp_code():
    first_digit = str(random.randint(1, 9))
    other_digits = [str(random.randint(0, 9)) for _ in range(4)]
    return first_digit + ''.join(other_digits)


def check_otp(data):
    if datetime.now() - data.order_by('-created_at').first().created_at > timedelta(hours=1):
        data.delete()
    if len(data) > 3:
        raise BadRequestException('Too many attempts! Please try after 1 hours.')


def check_user(user):
    if user is None:
        raise BadRequestException('User is required!')

    if not user.is_verified:
        raise BadRequestException('User is not verified!')


def check_otp_expired(otp):
    if datetime.now() - otp.created_at > timedelta(minutes=3):
        raise BadRequestException('OTP expired!')
