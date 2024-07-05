from rest_framework.routers import DefaultRouter

from api.application.verification.views import AppVerificationAPI

app_verification_router = DefaultRouter()

app_verification_router.register(prefix="", viewset=AppVerificationAPI, basename="login")
