# Generated by Django 4.1.3 on 2022-11-30 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0012_artistsprofile_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_photo_base64',
            field=models.TextField(null=True),
        ),
    ]
