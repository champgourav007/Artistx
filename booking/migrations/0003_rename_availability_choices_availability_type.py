# Generated by Django 4.1.3 on 2023-04-16 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_remove_availability_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availability',
            old_name='availability_choices',
            new_name='type',
        ),
    ]