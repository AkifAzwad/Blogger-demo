# Generated by Django 4.0 on 2021-12-27 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_rename_category_post_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='profile_pic',
            new_name='profile_picture',
        ),
    ]