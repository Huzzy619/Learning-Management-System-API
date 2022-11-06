from django.contrib import admin
from .models import *

admin.site.register ([Track, Course, Task, AnswerTask, Grade, UserCourse, Concept, Resource])