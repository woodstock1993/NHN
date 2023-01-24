from django.urls import path
from . import views
from . import views


urlpatterns = [
    path(
        'crawl',
        views.Board.as_view(),
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
    ),
    path(
        'seong-nam/<int:num>',
        views.SeongNamGetAPIView.as_view(),
        name='seong-nam'
    ),
    path(
        'gov/<int:num>',
        views.GovernmentGetAPIView.as_view(),
        name='gov'
    ),
    path(
        'bbc/<int:num>',
        views.BBCGetAPIView.as_view(),
        name='bbc'
    ),
]