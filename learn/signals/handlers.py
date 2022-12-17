from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver

from learn.models import Grade, Task

from ..tasks import send_email_for_graded_task, send_email_for_new_task


@receiver(post_save, sender=Task)
def new_task(instance, created, **kwargs):
    if created:
        try:
            send_email_for_new_task.delay(instance.id)

        except:
            pass

@receiver(post_save, sender=Grade)
def task_graded(instance, created, **kwargs):
    if created:
        try:
            send_email_for_graded_task.delay(instance.id)
        except:
            pass




