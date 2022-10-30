from celery import shared_task
from django.core.mail import EmailMessage, send_mail

from .models import Grade, Task, UserCourse


@shared_task
def send_email_for_new_task(id):
    print(id)
    task = Task.objects.get(id=id)

    user_list = UserCourse.objects.filter(course=task.course)

    user_emails = [item.user.email for item in user_list] + \
        ["hello@gmail.com", "Goodday@gmail.com"]

    for email in user_emails:
        message = EmailMessage(
            subject="New Task Created",
            body=f"Task title - {task.title}",
            to=[email]


        )
        message.send()


@shared_task
def send_email_for_graded_task(id):

    instance = Grade.objects.get(id=id)

    user_email = instance.answer.user.email

    task_title = instance.answer.task.title

    try:
        send_mail(
            subject="Your task has just been graded",
            message=f"Your task with title: {task_title} has just been graded \nYou Scored {instance.score}",
            from_email=None,
            recipient_list=[user_email]
        )
    except:
        pass


"""
@shared_task
def send_email_for_new_task():
    # task_course = instance.course

    # user_list = UserCourse.objects.filter(course=task_course)

    # user_emails = [item.user.email for item in user_list]

    print("I got here 1")
    message = EmailMessage(
        to=["blazingkrane@gmail.com"]  # single recipient...
        # ...multiple to emails would all get the same message
        # (and would all see each other's emails in the "to" header)
    )
    message.template_id = 1   # use this Sendinblue template
    message.from_email = None  # to use the template's default sender
    message.merge_global_data = {
        'name': "Alice",
        'order_no': "12345",
        'ship_date': "May 15",
    }

    print("I got here 2")
    message.send()
    
    print("I got here 3")



@shared_task
def send_email_for_graded_task(instance):
    user_email = instance.answer.user.email

    task_title = instance.answer.task.title

    try:
        send_mail(
            subject="Your task has just been graded",
            message=f"Your task with title: {task_title} has just been graded \nYou Scored {instance.score}",
            from_email=None,
            recipient_list=[user_email]
        )
    except:
        pass
"""
