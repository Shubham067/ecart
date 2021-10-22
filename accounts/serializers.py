from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User, update_last_login
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


class RegistrationSerializer(serializers.ModelSerializer):
    """Registration serializer requests and creates a new user."""

    # Ensure email is required and unique.
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="User with this email already exists.",
            )
        ],
    )

    # Ensure username is required and unique.
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="User with this username already exists.",
            )
        ],
    )

    # Ensure password is required, at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        required=True, max_length=128, min_length=8, write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    # token = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        # Use the `create_user` helper method of the `User` model's custom Manager to create a new user.
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ["id", "email", "username", "password"]


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "name", "is_admin"]
        # exclude = ['slug']

    def get_name(self, obj):
        name = obj.first_name

        if not name:
            name = obj.username

        return name

    def get_is_admin(self, obj):
        is_admin = obj.is_staff

        return is_admin


class LoginSerializer(serializers.ModelSerializer):
    """Login serializer authenticates and logs in a registered user."""

    name = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    email = serializers.EmailField(read_only=True)

    username = serializers.CharField(required=False)

    password = serializers.CharField(required=False, max_length=128, write_only=True)

    # token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` is "valid". In the case of logging a
        # user in, this means validating that they've provided a username
        # and password and that this combination matches one of the users in
        # our database.

        # email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password", None)

        # Raise an exception if an
        # email is not provided.
        # if email is None:
        #     raise serializers.ValidationError("An email address is required to log in.")

        # Raise an exception if a username is not provided.
        if username is None:
            raise serializers.ValidationError("A username is required to login.")

        # Raise an exception if a password is not provided.
        if password is None:
            raise serializers.ValidationError("A password is required to login.")

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this username/password combination.
        user = authenticate(username=username, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                "A user with this username and password doesn't exist!"
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated!")

        # Update the last login time of the user in the database every time
        # the user logs in.
        update_last_login(None, user)

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "is_staff": user.is_staff,
        }

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = [
            "id",
            "email",
            "username",
            "password",
            "name",
            "is_admin",
        ]

    def get_name(self, obj):
        name = obj.get("first_name")

        if not name:
            name = obj.get("username")

        return name

    def get_is_admin(self, obj):
        is_admin = obj.get("is_staff")

        return is_admin
