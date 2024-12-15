from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=250, null=False, blank=False)
    last_name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    profile_image = models.URLField(null=True)
    # Make this required when ready to go live
    phone_number = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=250, null=True)
    apartment = models.CharField(max_length=250, null=True)
    postal_code = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=250, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateField(auto_now=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + self.last_name
