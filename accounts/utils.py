import datetime
from random import randint

from kavenegar import *
from django.http import Http404
from django.conf import settings
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model


def otp_random_generator():
    return randint(1000, 9999)


def send_otp(mobile, otp):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {
            'sender': '1000596446',  # optional
            'receptor': [mobile, ],
            'message': f'Your OPT is: {otp}',
        }
        print(otp)
        # response = api.sms_send(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def is_expired(mobile):
    try:
        user = get_object_or_404(get_user_model(), mobile=mobile)
        diff_time = datetime.datetime.now().astimezone() - user.otp_create_time
        if diff_time.seconds > 30:
            return True
        return False
    except Http404:
        return False
