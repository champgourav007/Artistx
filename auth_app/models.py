import uuid
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=("user"), on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dob = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    currency_code = models.CharField(max_length=10, blank=True, null=True, default="INR")
    state = models.CharField(max_length=50, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="media/Profile", blank=True, null=True)
    profile_headline = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_artist = models.BooleanField(default=False)
    
    def get_age(self):
        curr_date = datetime.now()
        delta = curr_date - self.dob
        return delta.days
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class ArtistsProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=10, decimal_places=1)
    fee = models.DecimalField(max_digits=20, decimal_places=2)
    on_break = models.BooleanField(default=False)
    #availability column is pending for now will work in future
    
    def __str__(self):
        return f'{self.profile}'
    
class Language(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.profile} {self.language}'
    
class Review(models.Model):
    artist = models.ForeignKey(ArtistsProfile, on_delete=models.CASCADE)
    user_id = models.UUIDField(blank=True, null=True)
    rating = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=10)
    review = models.TextField()
    
    def __str__(self):
        return f'{self.artist}'