from django.urls import path, include

urlpatterns = [path("v1/twitter/", include("apps.twitter.api.v1.urls"))]
