from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerialier
from .models import User
from .utils import get_tokens_for_user
from helpers.utils import FSPageNumberPagination


@api_view(["POST"])
@authentication_classes([])
def register_user(request):
    context = {"exclude_fields": ["password"]}
    try:
        email = request.data.get("email")
        user_exists = User.objects.all().filter(email=email)
        if user_exists:
            return Response(
                {"message": "User with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        provider = request.data.get("provider")
        if provider is None:
            return Response(
                {"message": "provider is required to resgister a user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if provider == "password":
            user_serializer = UserSerialier(data=request.data, context=context)

            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                user = User.objects.get(email=email)
                tokens = get_tokens_for_user(user)
                return Response(
                    {**tokens, **user_serializer.data}, status=status.HTTP_201_CREATED
                )
    except Exception as e:
        # TODO: Handle Validation Errors
        print(f"Error================={e}")
        return Response({"message": "An error occurred"})


@api_view(["POST"])
@authentication_classes([])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"message": "Email and password are both required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user_exists = User.objects.get(email=email)

    if not user_exists:
        return Response(
            {"message": "User with this email not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    user = authenticate(email=email, password=password)

    if user is None:
        return Response(
            {"message": "Incorrect password"},
            status=status.HTTP_404_NOT_FOUND,
        )
    else:
        user.pop("password")
        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    queryset = User.objects.all().order_by("create_date")
    paginator = FSPageNumberPagination()
    # This endpoint is only accessible to staff accounts

    user = get_user(request=request)
    if not request.user.is_staff:
        paginated_queryset = paginator.paginate_queryset(
            queryset=queryset, request=request
        )
        print(paginator.get_paginated_response(list(paginated_queryset)))
        return paginator.get_paginated_response(list(paginated_queryset))
    return Response({})
