from django.db import models
from django.utils.translation import gettext_lazy as _

class UrlTarget(models.TextChoices):
    iam_school_1 = "https://school.iamservice.net/organization/1674/group/2001892", _("아이엠스쿨1")
    iam_school_2 = "https://school.iamservice.net/organization/19710/group/2091428", _("아이엠스쿨2")
    blog_1 = 'https://blog.naver.com/PostList.nhn?blogId=sntjdska123&from=postList&categoryNo=51', _("성남시블로그")
    blog_2 = 'https://blog.naver.com/PostList.nhn?blogId=hellopolicy&from=postList&categoryNo=168', _("정부블로그")
    bbc = 'http://feeds.bbci.co.uk/news/rss.xml', _("BBC")


class FuncTarget(models.TextChoices):
    IAMSCHOOL_1 = "iam_school_1", _("아이엠스쿨1")
    IAMSCHOOL_2 = "iam_school_2", _("아이엠스쿨2")
    BLOG_1 = "blog_1", _("성남시 블로그")
    BLOG_2 = "blog_2", _("정부 블로그")
    BBC = "bbc", _("BBC")


class Url(models.Model):
    name = models.CharField(max_length=32, null=False)
    url = models.URLField(primary_key=True, max_length=512, null=False)
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