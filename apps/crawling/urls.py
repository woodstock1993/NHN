from django.urls import path, include
from . import views
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path(
        'crawl',
        views.board.as_view(),
        name='crawl-get'
    ),
    path(
        'url',
        views.UrlCreateDeleteAPIView.as_view(),
        name='url-post'
    ),
    path(
        'iam_school_1/<int:num>',
        views.IamSchool_1APIView.as_view(),
        name='iam-school-1'
    )
]