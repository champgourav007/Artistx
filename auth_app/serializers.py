from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, ArtistsProfile, Language

class SignUpRequestSerailizer(serializers.Serializer):
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    dob = serializers.DateField(input_formats=['%Y-%m-%d',])
    email = serializers.EmailField()
    password = serializers.CharField(max_length=250)
    is_artist = serializers.BooleanField(default=False)
    
class SignUpResponseSerailizer(serializers.Serializer):
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    dob = serializers.DateField(input_formats=['%Y-%m-%d',])
    email = serializers.EmailField()
    profile_id = serializers.UUIDField()
    is_artist = serializers.BooleanField(default=False)
    access = serializers.CharField(max_length=1000)
    refresh = serializers.CharField(max_length=1000)
        
class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_photo',)
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('user','id')
        
class ArtistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistsProfile
        exclude = ('profile', 'id')
        
class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        exclude = ('profile', 'id')
        
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')