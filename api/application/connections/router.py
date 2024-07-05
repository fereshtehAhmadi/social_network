from rest_framework.routers import DefaultRouter

from api.application.connections.views import AppConnectionsAPI


app_connections_router = DefaultRouter()

app_connections_router.register(prefix="", viewset=AppConnectionsAPI, basename="connections")
