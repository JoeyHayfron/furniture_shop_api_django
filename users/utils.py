from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    token = RefreshToken.for_user(user)

    user = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username,
        "is_staff": user.is_staff,
    }
    token["user"] = user

    return {
        "access_token": str(token.access_token),
        "refresh_token": str(token),
    }


def decode_user_token(token):
    pass
