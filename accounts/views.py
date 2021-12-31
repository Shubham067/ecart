from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password


from .serializers import *


class CSRFTokenView(APIView):
    """Generate CSRF Token"""

    permission_classes = (AllowAny,)

    def get(self, request):
        response = JsonResponse({"status": "Success - Set CSRF cookie"})
        response["X-CSRFToken"] = get_token(request)
        return response


class RegistrationAPIView(generics.GenericAPIView):
    """Register a new user using this endpoint."""

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        # The create serializer, validate serializer, save serializer pattern
        # below is common.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": serializer.data,
                "status": status.HTTP_201_CREATED,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "accessExpiresIn": int(refresh.access_token.lifetime.total_seconds()),
            }
        )


class LoginAPIView(generics.GenericAPIView):
    """Login an existing user using this endpoint."""

    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.data["username"])

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": serializer.data,
                "status": status.HTTP_200_OK,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "accessExpiresIn": int(refresh.access_token.lifetime.total_seconds()),
            }
        )


class WhoAmIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        print(request.user.username)
        return Response(
            {"username": request.user.username, "status": status.HTTP_200_OK}
        )


class UserProfileView(APIView):
    """Get user profile details."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)

        return Response({"user": serializer.data, "status": status.HTTP_200_OK})


class UpdateUserProfileView(APIView):
    """Update user profile details."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user)

        data = request.data
        user.first_name = data["name"]
        user.username = data["username"]
        user.email = data["email"]

        if user.password != "" and data.get("password", "") != "":
            user.password = make_password(data["password"])

        user.save()

        return Response({"user": serializer.data, "status": status.HTTP_200_OK})


class UserListView(APIView):
    """Get a list of users."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)

        return Response({"users": serializer.data, "status": status.HTTP_200_OK})


class GetUserByIdView(APIView):
    """Get user details by id."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = self.serializer_class(user)

        return Response({"user": serializer.data, "status": status.HTTP_200_OK})


class UpdateUserView(APIView):
    """Update user details by id."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def put(self, request, pk):
        user = User.objects.get(id=pk)

        data = request.data

        user.first_name = data["name"]
        user.email = data["email"]
        user.is_staff = data["is_admin"]

        user.save()

        serializer = self.serializer_class(user)

        return Response({"user": serializer.data, "status": status.HTTP_200_OK})


class DeleteUserView(APIView):
    """Delete user by id."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        userToDelete = User.objects.get(id=pk)
        userToDelete.delete()

        return Response(
            {"detail": "User got deleted successfully", "status": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )
