from django.apps import AppConfig


class CrawlingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'crawling'
    name = 'apps.crawling'
