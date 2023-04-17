# Generated by Django 4.1.3 on 2023-04-16 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0017_profile_profile_photo_thumb_and_more'),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availability',
            name='date',
        ),
        migrations.RemoveField(
            model_name='availability',
            name='week_days',
        ),
        migrations.AlterField(
            model_name='availability',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_app.artistsprofile'),
        ),
        migrations.CreateModel(
            name='WeekDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.CharField(blank=True, choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], max_length=50, null=True)),
                ('availability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.availability')),
            ],
        ),
        migrations.CreateModel(
            name='Dates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('start_date', models.TimeField(blank=True, default='00:00:00', null=True)),
                ('end_date', models.TimeField(blank=True, default='59:59:00', null=True)),
                ('availability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.availability')),
            ],
        ),
    ]
