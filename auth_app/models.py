from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Users(models.Model):
    user = models.OneToOneField(User, verbose_name=("user"), on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    currency_code = models.CharField(max_length=10, blank=True, null=True, default="INR")
    state = models.CharField(max_length=50, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="media/Profile", blank=True, null=True)
    profile_headline = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_artist = models.BooleanField(default=False)
    
class ArtistsUser(models.Model):
    users = models.OneToOneField(Users, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=10, decimal_places=1)
    fee = models.DecimalField(max_digits=20, decimal_places=2)
    on_break = models.BooleanField(default=False)
    #availability column is pending for now will work in future
    

class Language(models.Model):
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    
class Review(models.Model):
    artist = models.ForeignKey(ArtistsUser, on_delete=models.CASCADE)
    review = models.TextField()