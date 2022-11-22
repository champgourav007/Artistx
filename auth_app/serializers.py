from rest_framework import serializers

class SignUpRequestSerailizer(serializers.Serializer):
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    dob = serializers.DateField(input_formats=['%Y-%m-%d',])
    email = serializers.EmailField()
    password = serializers.CharField(max_length=250)
    
class SignUpResponseSerailizer(serializers.Serializer):
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    dob = serializers.DateField(input_formats=['%Y-%m-%d',])
    email = serializers.EmailField()
    profile_id = serializers.UUIDField()
    access_token = serializers.CharField(max_length=1000)
    refresh_token = serializers.CharField(max_length=1000)