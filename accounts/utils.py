from random import randint

from kavenegar import *
from django.conf import settings


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
        response = api.sms_send(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
