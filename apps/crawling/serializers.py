from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.crawling.models import Post


class PostSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UrlSerializer(serializers.Serializer):
    url = serializers.URLField()