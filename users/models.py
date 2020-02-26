from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDERS = (
        (GENDER_MALE, "MALE"),
        (GENDER_FEMALE, "FEMALE"),
        (GENDER_OTHER, "OTHER"),
    )

    avatar = models.ImageField(null=True)
    gender = models.CharField(choices=GENDERS, null=True, max_length=10)
    bio = models.TextField(default="")
