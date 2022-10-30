from celery import shared_task
from core.models import *
from django.core.mail import EmailMessage
from learn.models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import render
from playground.tasks import notify_users, notify_users2


def test404 (request):
    return render(request, "404.html")



@permission_classes([AllowAny()])
@api_view()
def first(request):
    return Response({"Hello": "Hussein"})
    


@shared_task
def send():
    task = Task.objects.get(id = 1)

    task_course = task.course
    user_list = UserCourse.objects.filter(course = task_course)

    user_emails = [item.user.email for item in user_list] 

    EmailMessage(subject="hello",
    body="hi and welcome",
    to=user_emails+ ["who@djan.go"]).send()


def test(request):
    


    send.delay()

    notify_users.delay("Good Lord")

    notify_users2.delay("Second Message")

    from django.http import HttpResponse 
    return HttpResponse("Hello sombori")
        