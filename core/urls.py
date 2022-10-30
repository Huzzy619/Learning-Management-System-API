from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .social_view import GoogleLogin
from .views import *

router = DefaultRouter()

router.register("profile", ProfileViewSet, basename="profile")

nested_router = NestedDefaultRouter(router, "profile", lookup="user")

nested_router.register("picture", ImageViewSet, basename="profile_picture")
nested_router.register("employment-details", EmploymentViewSet,
                       basename="profile-employment_details")
nested_router.register("education", EducationViewSet,
                       basename="profile_education")
nested_router.register(
    "tech_history", Tech_HistoryViewSet, basename="profile_tech")
nested_router.register("social_links", SocialViewSet,
                       basename="profile_social")
nested_router.register("additional_info", InfoViewSet, basename="profile_info")

urlpatterns = [

    path("", include('dj_rest_auth.urls')),
    path("registration/students/", include('dj_rest_auth.registration.urls')),
    path("registration/mentor", MentorRegisterView.as_view()),
    # path("picture", ImageVie, name = "profile_pic")

    path('google/login', GoogleLogin.as_view(), name='google-rest')

]

urlpatterns += router.urls + nested_router.urls
