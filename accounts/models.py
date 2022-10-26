from datetime import datetime
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from learn.models import Course

from .managers import CustomBaseManager
from .validators import phone_validator

# Create your models here.


class User(AbstractUser):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female')

    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250, null=True, blank=True)
    phone = PhoneNumberField() #models.CharField(max_length=14, validators=[phone_validator])
    middle_name = models.CharField(max_length=250, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER)

    is_mentor = models.BooleanField(default = False)

    objects = CustomBaseManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def last_active():
        pass


class Image(models.Model):
    profile_pic = models.ImageField(upload_to="profile_pictures")
    user = models.OneToOneField(User, on_delete = models.CASCADE, default ='default.jpg') 


# PROFILE


class Employment (models.Model):
    organisation = models.CharField(max_length=550)
    role = models.CharField(max_length=550)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(
        validators=[MaxValueValidator(datetime.now().year)])
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Education (models.Model):
    school = models.CharField(max_length=550)
    course = models.CharField(max_length=550, help_text="BSC Computer Scinece")
    year_completed = models.PositiveIntegerField(
        validators=[MinValueValidator(2015)])

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Tech_History (models.Model):
    LONG = [
        ("1", "Less than one year"),
        ("1-3", "Between 1-3 years"),
        ("3-5", "Between 3-5 years"),
        ("5+", "5 years+")
    ]

    OS = [
        ("windows", "Windows OS"),
        ("mac", "Mac OS"),
        ("linux", "Linux OS")
    ]

    how_long = models.CharField(max_length=50, choices=LONG)

    os = models.CharField(max_length=30)

    reason = models.TextField()
    job_type = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Social (models.Model):
    github = models.URLField()
    linkedin = models.URLField()
    twitter = models.URLField()
    facebook = models.URLField()
    instagram = models.URLField()
    website = models.URLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Info (models.Model):
    alt_email = models.EmailField()
    alt_phone = PhoneNumberField() #models.CharField(max_length=14)
    country = CountryField() #models.CharField(max_length=30)
    nationality = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    address = models.TextField()
    disabiliies = models.CharField(max_length=500, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class UserCourse (models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'usercourse')