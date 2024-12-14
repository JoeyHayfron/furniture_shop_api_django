from django.urls import path, include


from .views import register_user, get_all_users

urlpatterns = [
    path(r"register/", register_user, name="register-user"),
    path(r"all/", get_all_users, name="get-all-users"),
]
