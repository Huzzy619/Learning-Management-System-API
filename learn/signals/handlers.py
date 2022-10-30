from django.dispatch import receiver
from django.db.models.signals import post_save
from learn.models import Grade, Task
from core.models import UserCourse
from django.core.mail import send_mail, EmailMessage


@receiver(post_save, sender=Task)
def new_task(instance, created, **kwargs):
    if created:
        task_course = instance.course

        user_list = UserCourse.objects.filter(course=task_course)

        user_emails = [item.user.email for item in user_list]

        try:
            send_mail(
            subject="hello",
            message="okay",
            from_email=None,  # "me@django.com",
            recipient_list=user_emails + ["who@djan.go"]
        )
        except:
            pass



@receiver(post_save, sender = Grade)
def task_graded(instance, created , **kwargs):
    if created:
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