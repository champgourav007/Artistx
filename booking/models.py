from django.db import models
from django.contrib.auth.models import User

from auth_app.models import ArtistsProfile
from constants.auth_app.models_choices import WEEK_DAYS
from constants.booking.availability_choices import AVAILABILITY_CHOICES


class Availability(models.Model):
  artist = models.ForeignKey(ArtistsProfile, on_delete=models.CASCADE)
  type = models.CharField(max_length=50, blank=True, null=True, choices=AVAILABILITY_CHOICES)
  
class Dates(models.Model):
  availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
  date = models.DateField(blank=True, null=True)
  start_time = models.TimeField(blank=True, null=True, default="00:00:00")
  end_time = models.TimeField(blank=True, null=True, default="23:59:00")
  
class WeekDays(models.Model):
  availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
  week_day = models.CharField(max_length=50, choices=WEEK_DAYS, blank=True, null=True)

class Event(models.Model):
  artist = models.OneToOneField(ArtistsProfile, on_delete=models.CASCADE)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  event_date = models.DateField()
  event_time = models.TimeField()
  event_location = models.CharField(max_length=255)
  event_directions = models.CharField(max_length=255, blank=True, null=True)
  audio_instructions = models.URLField(blank=True, null=True)
  expected_footfall = models.IntegerField(blank=True, null=True)
  event_duration = models.DecimalField(max_digits=100000,decimal_places=2, blank=True, null=True)
  accomodation = models.CharField(max_length=200, blank=True, null=True)
  accomodation_address = models.TextField(blank=True, null=True)
  