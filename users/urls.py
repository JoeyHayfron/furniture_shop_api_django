from django.urls import path, include


from .views import register_user, get_all_users, get_or_update_user, login_user

urlpatterns = [
    path(r"register/", register_user, name="register-user"),
    path(r"login/", login_user, name="login-user"),
    path(r"all/", get_all_users, name="get-all-users"),
    path(r"<int:pk>/", get_or_update_user, name="get-or-update-user"),
]
