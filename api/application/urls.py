from django.urls import path
from django.urls.conf import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from api.application.search_users.router import app_search_users_router
from api.application.request_manager.router import app_request_manager_router
from api.application.user_profile.router import app_profile_router
from api.application.verification.router import app_verification_router


app_common_urls = [
    path("verification/", include(app_verification_router.urls)),
    path("profile/", include(app_profile_router.urls)),
    path("app_search_users_router/", include(app_search_users_router.urls)),
    path("request_manager/", include(app_request_manager_router.urls)),
]

app_urls = app_common_urls

app_schema_view = get_schema_view(
    openapi.Info(
        title="Social Network App",
        default_version="v1",
        description="اپلیکیشن شبکه اجتماعی",
    ),
    public=True,
    permission_classes=[AllowAny],
    patterns=[path("social_network/api/app/", include(app_urls))],
)
