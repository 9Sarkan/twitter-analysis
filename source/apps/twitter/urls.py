from django.urls import path, include

urlpatterns = [path("", include("apps.twitter.api.v1.urls"))]
