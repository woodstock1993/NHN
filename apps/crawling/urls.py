from django.urls import path
from . import views

urlpatterns = [
    path(
        'crawl/',
        views.board.as_view(),
        name='crawl-get'
    ),
]