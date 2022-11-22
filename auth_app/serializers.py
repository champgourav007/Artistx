from rest_framework import serializers
from .models import Profile

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
    access_token = serializers.CharField(max_length=1000)
    refresh_token = serializers.CharField(max_length=1000)
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("user", "id", "is_email_verified", "profile_photo")