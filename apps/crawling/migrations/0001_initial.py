# Generated by Django 4.1.5 on 2023-01-22 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('name', models.CharField(max_length=32)),
                ('url', models.URLField(max_length=512, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
            ],
            options={
                'db_table': 'url',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='게시글 제목')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('published_datetime', models.DateTimeField(blank=True, null=True, verbose_name='출판일')),
                ('body', models.TextField(blank=True, verbose_name='HTML')),
                ('attachment_list', models.JSONField(null=True, verbose_name='파일 이름')),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='crawling.url', verbose_name='게시글이 있는 url')),
            ],
            options={
                'db_table': 'post',
            },
        ),
    ]