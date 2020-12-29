from django.urls import path, include

urlpatterns = [path("v1/sample-app/", include("apps.sample-app.api.v1.urls"))]
