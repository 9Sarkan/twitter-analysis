from rest_framework.views import APIView
from apps.twitter.adapter import TwitterAdapter
from rest_framework.response import Response
from rest_framework import status
from apps.twitter import models


class GetMostCommons(APIView):
    def get(self, request, *args, **kwargs):
        tag = kwargs.get("tag")
        limit = request.GET.get("limit", 20)
        if not tag:
            return Response(
                {"code": 400, "message": "tag required"}, status.HTTP_400_BAD_REQUEST
            )
        tag_qs = models.Tag.objects.filter(slug=tag)
        if not tag_qs.exists():
            return Response(
                {"code": 404, "message": "tag not found"}, status.HTTP_404_NOT_FOUND
            )
        tag_obj = tag_qs.first()
        data = TwitterAdapter().get_most_common(tag, tag_obj.collection, limit)
        return Response(data)


class GetFromPopulars(APIView):
    def get(self, request, *args, **kwargs):
        tag = kwargs.get("tag")
        limit = request.GET.get("limit", 20)
        tag_qs = models.Tag.objects.filter(slug=tag)
        if not tag_qs.exists():
            return Response(
                {"code": 404, "message": "tag not found"}, status.HTTP_404_NOT_FOUND
            )
        tag_obj = tag_qs.first()
        data = TwitterAdapter().get_from_populars(tag, limit)
        return Response(data)


class GetMostRetweeted(APIView):
    def get(self, request, *args, **kwargs):
        tag = kwargs.get("tag")
        limit = request.GET.get("limit", 20)
        tag_qs = models.Tag.objects.filter(slug=tag)
        if not tag_qs.exists():
            return Response(
                {"code": 404, "message": "tag not found"}, status.HTTP_404_NOT_FOUND
            )
        tag_obj = tag_qs.first()
        data = TwitterAdapter().get_most_retweet(tag, limit)
        return Response(data)
