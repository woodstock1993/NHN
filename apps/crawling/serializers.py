from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.crawling.models import Post

class UrlTarget(models.TextChoices):
    iamSCHOOL_1 = "https://school.iamservice.net/organization/1674/group/2001892", _("아이엠스쿨1")
    iamSCHOOL_2 = "https://school.iamservice.net/organization/19710/group/2091428", _("아이엠스쿨2")
    BLOG_1 = 'https://blog.naver.com/PostList.nhn?blogId=sntjdska123&from=postList&categoryNo=51', _("성남시블로그")
    BLOG_2 = 'https://blog.naver.com/PostList.nhn?blogId=hellopolicy&from=postList&categoryNo=168', _("정부블로그")
    BBC = 'http://feeds.bbci.co.uk/news/rss.xml', _("BBC")


class PostSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UrlSerializer(serializers.Serializer):
    url = serializers.URLField()