from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings

User = settings.AUTH_USER_MODEL



class Track (models.Model):
    name = models.CharField(max_length = 250)
    description = models.CharField(max_length = 250)

    def __str__(self) -> str:
        return self.name

class Course (models.Model):
    title = models.CharField(max_length = 550)
    track = models.ForeignKey(Track, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Task (models.Model):

    SUBMISSION = [
        ("URL" ,"URL"),
        ("TEXT", "TEXT")
    ]

    title = models.CharField(max_length = 550)
    content = models.TextField()
    created_on  = models.DateTimeField(auto_now_add = True)
    course = models.ForeignKey(Course, on_delete = models.DO_NOTHING)
    mode_of_submission = models.CharField(max_length = 50, choices = SUBMISSION)
    

    created_by = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    submission_date = models.DateTimeField()
    total_grade = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return self.title

class AnswerTask (models.Model):
    task = models.ForeignKey(Task, on_delete = models.CASCADE, related_name = "answer")
    answer = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        unique_together = [['user', 'task']]

class Grade (models.Model):
    graded_by = models.ForeignKey(User, on_delete = models.DO_NOTHING )
    score = models.PositiveIntegerField()
    feedback = models.TextField(null = True, blank = True)
    answer = models.OneToOneField(AnswerTask, on_delete = models.CASCADE)
    regraded = models.BooleanField(default = False)


class UserCourse (models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'usercourse')


class Concept (models.Model):
    link = models.URLField()
    task = models.ManyToManyField(Task, related_name = "concepts")


class Resource (models.Model):
    link= models.URLField()
    task = models.ManyToManyField(Task, related_name = 'resources')
