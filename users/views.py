# from django.shortcuts import render
from django.contrib.auth import authenticate
from django.db.models import Q

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .serializers import UserSerializer, UserSerializerWithoutPassword
from .models import User
from .utils import get_tokens_for_user
from helpers.utils import FSPageNumberPagination


@api_view(["POST"])
@authentication_classes([])
def register_user(request):
    try:
        email = request.data.get("email")
        user_exists = User.objects.all().filter(email=email)

        if user_exists:
            return Response(
                {"message": "User with this email or username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        provider = request.data.get("provider")
        if provider is None:
            return Response(
                {"message": "provider is required to register a user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if provider == "password":
            user_serializer = UserSerializer(
                data=request.data,
            )

            if user_serializer.is_valid(raise_exception=True):
                user = user_serializer.save()
                tokens = get_tokens_for_user(user)
                user_data_without_password = UserSerializerWithoutPassword(
                    user_serializer.data
                )
                return Response(
                    {**tokens, **user_data_without_password.data},
                    status=status.HTTP_201_CREATED,
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

    print(user_exists.check_password(password))

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
        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    queryset = User.objects.all().order_by("create_date")
    paginator = FSPageNumberPagination()
    search_query = request.query_params.get("q", None)

    if search_query:
        queryset = queryset.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
        )

    paginated_queryset = paginator.paginate_queryset(queryset=queryset, request=request)
    user_serialized_data = UserSerializerWithoutPassword(paginated_queryset, many=True)
    print(paginator.get_paginated_response(user_serialized_data.data))
    return paginator.get_paginated_response(user_serialized_data.data)


@api_view(["GET", "PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_or_update_user(request, pk):
    req_user = request.user
    user_from_pk = User.objects.get(id=pk)

    if not req_user.is_staff and user_from_pk.id != req_user.id:
        return Response(
            {"message": "Only admins and account owners can view or edit account"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user_from_pk:
        return Response(
            {"message": "User with this id does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        if request.method == "PATCH":
            user_serializer = UserSerializer(
                user_from_pk, data=request.data, partial=True
            )
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                user_data = UserSerializerWithoutPassword(user_serializer.data)
                return Response(user_data.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Please ensure "})

        if request.method == "GET":
            user_serializer = UserSerializerWithoutPassword(user_from_pk)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
    except ValidationError as err:
        errors = dict(err.detail)
        errors_dict = {}
        for key, value in errors.items():
            errors_dict[key] = value[0]
        return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"message": f"An error occurred {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
