from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Ecart API")

urlpatterns = [
    url(r"^$", schema_view),
    path("admin/", admin.site.urls),
    path("api/", include("store.urls", namespace="store")),
    path("api/accounts/", include("accounts.urls", namespace="accounts")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
