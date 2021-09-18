from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path(
        "get-most-commons/<str:tag>/",
        views.GetMostCommons.as_view(),
        name="get-most-commons",
    ),
    path(
        "get-from-populars/<str:tag>/",
        views.GetFromPopulars.as_view(),
        name="get-from-populars",
    ),
    path(
        "get-most-populars/<str:tag>/",
        views.GetMostRetweeted.as_view(),
        name="get-most-populars",
    ),
]
