# Generated by Django 4.0 on 2022-01-02 18:21

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(default='test', verbose_name='Content'),
            preserve_default=False,
        ),
    ]