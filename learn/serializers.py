from django.core.validators import URLValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.utils import IntegrityError

from .models import *


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        exclude = ['created_by']

    def save(self, **kwargs):

        if self.context['user'].is_mentor:

            return super().save(created_by=self.context['user'], **kwargs)

        raise serializers.ValidationError("Only mentors can create tasks")


class GradeSerializer (serializers.ModelSerializer):
    class Meta:
        model = Grade
        exclude = ["answer", "graded_by"]

    def save(self, **kwargs):
        return super().save(
            graded_by=self.context['request'].user,
            answer_id=self.context['answer_pk'],
            **kwargs
        )


class AnswerTaskSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AnswerTask
        fields = ['task', 'answer', 'grade', 'user']

    def get_user(self, obj):
        return obj.user.email

    def save(self, **kwargs):

        user = self.context['user']

        # check if task is expired

        task = Task.objects.get(pk=self.context['task_pk'])
        if timezone.now() >= task.submission_date:
            raise serializers.ValidationError("Task Expired")

        # checking if the answer matches the mode of submission

        if task.mode_of_submission == "URL":
            validate = URLValidator()
            try:
                validate(self.validated_data['answer'])
            except:
                raise serializers.ValidationError(
                    "An active link must be submitted for this tasks")

        elif task.mode_of_submission == "TEXT":
            # checks if there is a link in the submission
            try:
                validate = URLValidator(inverse_match=True)
                validate(self.validated_data['answer'])

            except:
                raise serializers.ValidationError(
                    "A plain text is expected not an url")
        try:

            return super().save(task=task, user=user, **kwargs)

        except IntegrityError:  # this is from the unique together constraint set in the model
            raise serializers.ValidationError(
                "You have already provided your answer to this task")


class CourseEnrollSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only = True)
    course_title = serializers.SerializerMethodField()
    class Meta:
        model = UserCourse
        fields = ["id","user_name","course", "course_title"]
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()
    
    def get_course_title(self, obj):
        return obj.course.title

    def save(self, **kwargs):
        return super().save(user=self.context['user'], **kwargs)
