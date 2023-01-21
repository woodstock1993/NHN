from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.crawling.models import Post, Url


class PostSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["title", "published_datetime", "body", "attachment_list"]

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res.update({"url": UrlSerializer(instance.url).data})
        return res


class OriginUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = "__all__"

class UrlSerializer(serializers.Serializer):
    url = serializers.CharField()