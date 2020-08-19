from django.conf import settings

import kavenegar


def send_sms(phone_number, message):
    try:
        api = kavenegar.KavenegarAPI(settings.KAVENEGAR_APIKEY)
        message = message
        params = {
            'sender': '1000596446',
            'receptor': phone_number,
            'message': message,
        }
        response = api.sms_send(params)
        print(response)
    except kavenegar.APIException as e:
        print(e)
    except kavenegar.HTTPException as e:
        print(e)
