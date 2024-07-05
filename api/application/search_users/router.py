from rest_framework.routers import DefaultRouter

from api.application.search_users.views import AppSearchUsersAPI


app_search_users_router = DefaultRouter()

app_search_users_router.register(prefix="", viewset=AppSearchUsersAPI, basename="search_users")
