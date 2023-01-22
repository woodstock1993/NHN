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
        'sunae/<int:num>',
        views.SunaeGetAPIView.as_view(),
        name='sunae'
    ),
    path(
        'yongin/<int:num>',
        views.YonginGetAPIView.as_view(),
        name='youngin'
    )
]