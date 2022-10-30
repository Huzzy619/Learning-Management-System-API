from time import sleep
from LMS.celery import celery
from celery import shared_task

@celery.task
def notify_users(message):
    print('sending 1Million emails.....')
    print(message)
    sleep(20)
    print("Emails delivered successfuly")

@shared_task
def notify_users2(message):
    print('sending 100,000 emails.....')
    print(message)
    sleep(20)
    print("Emails delivered successfuly")