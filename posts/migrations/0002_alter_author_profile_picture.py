# Generated by Django 4.0 on 2022-01-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profile_picture',
            field=models.ImageField(default='avatar.jpg', upload_to=''),
        ),
    ]
