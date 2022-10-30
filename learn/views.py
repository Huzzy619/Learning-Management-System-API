
from email import message
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from .models import *
from .pagination import TaskPaginator
from .permissions import IsMentor, IsStudent
from .serializers import *
from learn.signals import new_signal
from django.core.mail import EmailMessage
def test(request):
    # new_signal.send_robust(__name__)
    for email in ["huzzy@django.com", "kola@go.com"]:
        message = EmailMessage(
            subject="New Task Created",
            body=f"Task title - ",
            to= [email]
            
        )
        message.send()

        print(email)

    return HttpResponse(" Seems to be working just fine")


class TaskViewSet (ModelViewSet):
    """
    Task can be created, updated, and deleted by Mentors.

    Students will see only tasks on their registered courses.

    """
    pagination_class = TaskPaginator
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
                user_answers = task.answer.filter(
                    user=request.user).select_related('user', 'grade')
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

    def get_permissions(self):
        if not self.request.method in permissions.SAFE_METHODS:
            return [IsMentor()]
        return [permissions.IsAuthenticated()]


class AnswerTaskViewSet (ModelViewSet):
    # http_method_names = ['post'] # Answers cannot be edited or updated or deleted
    """
    Only Students can POST their answers to tasks, Mode of submission (URL or Text)

    Filter by user and task, Also search by task(title and submission_date)
    """
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user', 'task']
    http_method_names = ['post', 'get', 'options', 'head']
    pagination_class = TaskPaginator
    permission_classes = [IsStudent]
    search_fields = ['task__title', 'task__submisson_date']
    serializer_class = AnswerTaskSerializer

    def get_queryset(self):
        answer = AnswerTask.objects.all().select_related('user', 'task', 'grade')

        if self.request.user.is_mentor:
            return answer
        return answer.filter(user=self.request.user)

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

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsMentor()]


class CourseEnrollViewSet(ModelViewSet):
    http_method_names = ['post', 'delete', 'get']
    serializer_class = CourseEnrollSerializer
    queryset = UserCourse.objects.all().select_related('course', 'user')

    def get_serializer_context(self):
        return {'user': self.request.user}