from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import *

router = DefaultRouter()

router.register("task",TaskViewSet, basename='task')

answer_router = NestedDefaultRouter(router, "task", lookup = "task")
answer_router.register("answer", AnswerTaskViewSet, basename="task-answer")

grade_router = NestedDefaultRouter(answer_router, "answer", lookup = "answer")
grade_router.register("grade", GradeViewSet, basename="answer-grade" )

urlpatterns = [
    
]

urlpatterns += router.urls + answer_router.urls + grade_router.urls