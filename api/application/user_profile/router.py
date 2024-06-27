from rest_framework.routers import DefaultRouter

from api.application.user_profile.views import AppProfileAPI

app_profile_router = DefaultRouter()

app_profile_router.register(prefix="profile", viewset=AppProfileAPI, basename="profile")
