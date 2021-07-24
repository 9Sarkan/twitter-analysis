from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TestAPI


router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("test/", TestAPI.as_view(), name="test"),
]
