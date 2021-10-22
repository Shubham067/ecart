from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("register/", RegistrationAPIView.as_view()),
    path("csrf/", CSRFTokenView.as_view(), name="get_csrf_token"),
    path("login/", LoginAPIView.as_view()),
    path("whoami/", WhoAmIView.as_view(), name="whoami"),
    path("user/profile/", UserProfileView.as_view(), name="user_profile"),
    path(
        "user/profile/update/",
        UpdateUserProfileView.as_view(),
        name="update_user_profile",
    ),
    path("users/", UserListView.as_view(), name="all_users"),
    path("user/<str:pk>/", GetUserByIdView.as_view(), name="get_user_by_id"),
    path("users/update/<str:pk>/", UpdateUserView.as_view(), name="update_user"),
    path("users/delete/<str:pk>/", DeleteUserView.as_view(), name="delete_user"),
]
