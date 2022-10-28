from rest_framework import serializers
from .models import *
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer


class CustomLoginSerializer (LoginSerializer):
    username = None  # Remove username from the login


class MentorRegisterSerializer(RegisterSerializer):

    def save(self, request):
        user = super().save(request)

        user.is_mentor = True
        user.save()
        return user


class ProfileSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name',
                  'middle_name', 'phone', 'gender']

    # def save(self, **kwargs):

    #     user_id = self.context['user_id']
    #     instance = User.objects.update(id = user_id , **self.validated_data)
    #     return instance


class ImageSerializer (serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'user', 'profile_pic']


class AddImageSerializer (serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['profile_pic']

    def save(self, **kwargs):
        if img := Image.objects.filter(user=self.context['user']):

            return img.update(**self.validated_data)

        return super().save(user=self.context['user'], **kwargs)


class EmploymentSerializer (serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = ['id', "organisation", 'role', 'start_year', 'end_year']

    def save(self, **kwargs):
        if employment := Employment.objects.filter(user=self.context['user']):

            return employment.update(**self.validated_data)

        return super().save(user=self.context['user'], **kwargs)


class EducationSerializer (serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'school', 'course', 'year_completed']

    def save(self, **kwargs):
        return super().save(user=self.context['user'], **kwargs)


class TechSerializer (serializers.ModelSerializer):
    class Meta:
        model = Tech_History
        fields = ['id', 'how_long', 'os', 'reason', 'job_type']

    def save(self, **kwargs):
        if tech := Tech_History.objects.filter(user=self.context['user']):
            return tech.update(**self.validated_data)

        return super().save(user=self.context['user'], **kwargs)


class SocialSerializer (serializers.ModelSerializer):
    class Meta:
        model = Social
        exclude = ['user']

    def save(self, **kwargs):
        if social := Social.objects.filter(user=self.context['user']):
            return social.update(**self.validated_data)

        return super().save(user=self.context['user'], **kwargs)


class InfoSerializer (serializers.ModelSerializer):
    class Meta:
        model = Info
        exclude = ['user']

    def save(self, **kwargs):
        if info := Info.objects.filter(user=self.context['user']):
            return info.update(**self.validated_data)

        return super().save(user=self.context['user'], **kwargs)


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
