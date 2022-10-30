from dj_rest_auth.registration.views import RegisterView
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permissions import IsOwner
from .serializers import *


class MentorRegisterView(RegisterView):
    """
    Mentors Should register here to get some level of permission.

    """
    serializer_class = MentorRegisterSerializer


class ProfileViewSet (ModelViewSet):
    """
    Users can update their informations 

    """
    http_method_names = ['get','patch','options', 'head']
    permission_classes = [IsOwner]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class ImageViewSet (ModelViewSet):
    """
    upload and update profile picture

    """
    queryset = Image.objects.filter()
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddImageSerializer
        return ImageSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}


class EmploymentViewSet (ModelViewSet):
    """

    Fill in to create or update employment details

    """

    http_method_names = ['get','post','patch','options', 'head']
    permission_classes = [IsOwner]
    serializer_class = EmploymentSerializer

    def get_queryset(self):
        return Employment.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class EducationViewSet(ModelViewSet):

    """
    Provide or edit Educational endeavours

    """
    http_method_names = ['get','post','patch','options', 'head']
    permission_classes = [IsOwner]
    serializer_class = EducationSerializer

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class Tech_HistoryViewSet (ModelViewSet):
    """
    Have some experience in Tech? Tell us how much experience you've got

    """
    http_method_names = ['get','post','patch','options', 'head']
    permission_classes = [IsOwner]
    serializer_class = TechSerializer

    def get_queryset(self):
        return Tech_History.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class SocialViewSet (ModelViewSet):
    """
    Save and update Social Media Profiles 

    """
    http_method_names = ['get','post','patch','options', 'head']
    permission_classes = [IsOwner]
    serializer_class = SocialSerializer

    def get_queryset(self):
        return Social.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class InfoViewSet (ModelViewSet):
    """
    Additional Information of Users

    """
    http_method_names = ['get','post','patch','options', 'head']
    permission_classes = [IsOwner]
    serializer_class = InfoSerializer

    def get_queryset(self):
        return Info.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}



