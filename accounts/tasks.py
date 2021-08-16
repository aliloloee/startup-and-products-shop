from django.conf import settings
from django.utils import timezone

from customUser.models import User

from celery import shared_task
from random import randint
from datetime import timedelta

from BANPars.redis_conf import redis
from kavenegar import *




def generate_otp():
    return str(randint( pow(10,settings.OTP_LENGTH-1) , pow(10, settings.OTP_LENGTH)-1 ))


# Do not forget to delete the prints in send_otp function
@shared_task
def send_otp(mobile) : 
    otp = generate_otp()
    receptor = [mobile, ]
    try :
        # api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        # # tip : take the language and send translated message to the user
        # params = {'sender': '1000596446', 'receptor': receptor, 'message': f'Your OTP is {otp}'}
        # response = api.sms_send(params)
        redis.set(f'{mobile}', f'{otp}', ex=settings.OTP_EXPIRATION_TIMESTAMP, nx=True)
        print(f'OTP : {otp}')
        # print(response)
    except APIException as e :
        print(e)
    except HTTPException as e :
        print(e)

@shared_task
def clear_not_activated_users() :
    time_threshold = timezone.now() - timedelta(hours=settings.NOT_ACTIVATED_USERS_THERESHOLD)
    results = User.objects.filter(is_active=False, date_joined__lte=time_threshold)
    results.delete()



@shared_task
def say_hi() :
    print('hi')
