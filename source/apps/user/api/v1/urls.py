from django.urls import path, include, re_path
from apps.user.api.v1 import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.UserViewSet, basename="users")

urlpatterns = [
    re_path(
        r"change-password/(?P<user_id>\d{1,})/(?P<token>\d{5})/$",
        views.reset_password,
    ),
    path("forget-password/", views.forget_password_get_code),
    # router
    path("user/", include(router.urls)),
]
