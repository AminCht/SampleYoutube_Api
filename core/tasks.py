import datetime
from time import sleep
from celery import shared_task
from django.core.mail import send_mail, BadHeaderError

from app.models import AppUser


@shared_task()
def notify_birth_day(message):
    queryset = AppUser.objects.filter(birth_date__month=datetime.date.today().month, birth_date__day=datetime.date.today().day)
    print(list(queryset))
    try:
        for key in list(queryset):
            print(key)
            send_mail('subject', f'HBD {key.user.first_name}', 'amincht81@gmail.com', [key.user.email])
        print('email sent')
    except BadHeaderError:
        pass


