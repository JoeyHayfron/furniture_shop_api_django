from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import User

# Register your models here.


class UserAdmin(ModelAdmin):
    list_display = ("first_name", "last_name", "username", "email")
    search_fields = ("first_name", "username", "email")


admin.site.register(User, UserAdmin)
