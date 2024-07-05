from rest_framework.routers import DefaultRouter

from api.application.request_manager.views import AppRequestManagerAPI

app_request_manager_router = DefaultRouter()

app_request_manager_router.register(prefix='', viewset=AppRequestManagerAPI, basename="request_manager")
