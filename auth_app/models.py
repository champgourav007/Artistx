import uuid
from django.contrib.auth.models import User
from django.db import models
from datetime import date


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=("user"), on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dob = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    currency_code = models.CharField(max_length=10, blank=True, null=True, default="INR")
    state = models.CharField(max_length=50, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="Profile/", blank=True, null=True)
    profile_photo_base64 = models.TextField(null=True)
    profile_headline = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_artist = models.BooleanField(default=False, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False, null=True, blank=True)
    
    def get_age(self):
        curr_date = date.today()
        dob = self.dob
        return (curr_date - dob).days // 365
    
    def name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.user.email}'
    
class ArtistsProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    fee = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    on_break = models.BooleanField(default=False, blank=True, null=True)
    
    GENRE = (
        ("Photography", "Photography"), 
        ("Cinematography", "Cinematography"), 
        ("DJ", "DJ"), 
        ("Singer", "Singer"), 
        ("Dancer", "Dancer"), 
        ("Choreographers", "Choreographers"),
        ("Others", "Others"))
    genre = models.CharField(max_length=255, choices=GENRE, default="Photography")
    #availability column is pending for now will work in future
    
    def __str__(self):
        return f'{self.profile}'
    
    def artist_rating(self, artist):
        tot_rating = Review.objects.filter(artist = artist).aggregate(models.Sum('rating'))
        tol_people_rated = Review.objects.filter(artist = artist).aaggregate(models.Count('rating'))
        return tot_rating / tol_people_rated
        
    
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

class Otp(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    otp = models.IntegerField(null=True)
    valid_upto = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now=True, null=True)