from collections import OrderedDict
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from accounts.models import UserCourse
from .serializers import *
from .models import *
from rest_framework.views import APIView


class TaskViewSet (ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @action(detail=False)
    def me(self, request, **kwargs):
        if request.method == "GET":

            # Get the user's registered courses

            # The distinct may not be needed.
            user_courses = UserCourse.objects.filter(
                user=request.user).values('course').distinct()

            # Filter the task according to the courses offered by the user
            tasks = Task.objects.filter(
                course__in=user_courses)  # .annotate(hello = 1)

            serializer = self.get_serializer(tasks, many=True)

        return Response(serializer.data)

    @action(detail=False)
    def my_info(self, request):
        if request.method == "GET":

            # Get the user's registered courses

            # The distinct may not be needed.
            user_courses = UserCourse.objects.\
                filter(user=request.user).values('course').distinct()

            # Filter the task according to the courses offered by the user
            tasks = Task.objects.filter(
                course__in=user_courses)  # .annotate(hello = 1)

            # total attainable scores
            total = sum([task.total_grade for task in tasks])

            scores_of_user = []

            for task in tasks:
                # get answers of the current users
                user_answers = task.answer.filter(user=request.user).select_related('user', 'grade')
                print(user_answers)
                for answer in user_answers:
                    try:
                        # try to get scores of those answers
                        scores_of_user.append(answer.grade.score)
                    except:
                        # catch the exception that will be throwed if any of the answers have not been graded, and skip it then continue the loop
                        continue

            total_scores = sum(scores_of_user)

        return Response(
            {
            "total_attainable_score": total, 
            "total_scores_gotten": total_scores,
            "number_of_courses": user_courses.count(),
            # "number_of_task_attempted": user_answers.count()
            }
            )

    def get_serializer_context(self):
        # had to pass total as None to avoid Key erorr in the serializer
        return {'user': self.request.user}


class AnswerTaskViewSet (ModelViewSet):
    http_method_names = ["post","get", "head", "options"] # Answers cannot be edited or updated or deleted
    serializer_class = AnswerTaskSerializer

    def get_queryset(self):
        if self.request.user.is_mentor :
            return AnswerTask.objects.all().select_related('user', 'task', 'grade')
        return AnswerTask.objects.filter(user = self.request.user).select_related('user', 'task', 'grade')
        
    def get_serializer_context(self):
        context = {
            'user': self.request.user,
            'task_pk': self.kwargs['task_pk'],
        }
        return context

    



class GradeViewSet (ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_serializer_context(self):
        return {'answer_pk': self.kwargs['answer_pk'], 'request': self.request}
