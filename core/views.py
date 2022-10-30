from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from dj_rest_auth.registration.views import RegisterView


from .models import *
from .serializers import * 


class MentorRegisterView(RegisterView):
    serializer_class = MentorRegisterSerializer


class ProfileViewSet (ModelViewSet):
    # http_method_names = ['put','head','get','options','patch']
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class ImageViewSet (ModelViewSet):
    queryset = Image.objects.filter()

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddImageSerializer
        return ImageSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}


class EmploymentViewSet (ModelViewSet):
    serializer_class = EmploymentSerializer

    def get_queryset(self):
        return Employment.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class EducationViewSet(ModelViewSet):
    serializer_class = EducationSerializer

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class Tech_HistoryViewSet (ModelViewSet):
    serializer_class = TechSerializer

    def get_queryset(self):
        return Tech_History.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class SocialViewSet (ModelViewSet):
    serializer_class = SocialSerializer

    def get_queryset(self):
        return Social.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class InfoViewSet (ModelViewSet):
    serializer_class = SocialSerializer

    def get_queryset(self):
        return Info.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class CourseEnrollViewSet(ModelViewSet):
    http_method_names = ['post', 'delete', 'get']
    serializer_class = CourseEnrollSerializer
    queryset = UserCourse.objects.all().select_related('course', 'user')

    def get_serializer_context(self):
        return {'user': self.request.user}
