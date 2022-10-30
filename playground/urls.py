from .views import first, test404
from django.urls import path



urlpatterns = [
    path("f", first),
    path("t", test404),
]


