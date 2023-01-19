from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Url(models.Model):
    url = models.URLField(max_length=512, null=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class  Meta:
        db_table = "url"

class Post(models.Model):
    title = models.CharField(max_length=64, verbose_name="게시글 제목")
    created = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    published_datetime = models.DateTimeField(null=True, blank=True, verbose_name="출판일")
    body = models.TextField(verbose_name="HTML")
    attachment_list = models.JSONField(verbose_name="파일 이름")
    url = models.ForeignKey(
        Url,
        related_name="post",
        on_delete=models.CASCADE,
        verbose_name='게시글이 있는 url'
    )

    class Meta:
        db_table = 'post'
    