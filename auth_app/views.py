from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpRequestSerailizer, SignUpResponseSerailizer
from .models import Profile

# Create your views here.
@api_view(['POST'])
def signup(request):
    '''Function for signup'''
    serializer = SignUpRequestSerailizer(data=request.POST)
    
    if serializer.is_valid():
        try:
            user = User.objects.create_user(
                username = serializer.data.get('email'),
                first_name = serializer.data.get('first_name'),
                last_name = serializer.data.get('last_name'),
                email = serializer.data.get('email'),
                password = serializer.data.get('password'),
            )
            user.save()
            
            profile = Profile.objects.create(
                user = user,
                dob = serializer.data.get('dob'),
            )
            profile.save()
            
            response = SignUpResponseSerailizer(data={
                'first_name' : serializer.data.get('first_name'),
                'last_name' : serializer.data.get('last_name'),
                'email' : serializer.data.get('email'),
                'dob' : serializer.data.get('dob'),
                'profile_id' : profile.id
            })
            
            if response.is_valid():
                return Response(data=response.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(data="Some Error Occured", 
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
                            
        except:
            return Response(data={
                    'message' : 'User Already Exists',
                },
                status=status.HTTP_208_ALREADY_REPORTED)
        
    return Response(data=serializer.error_messages,
                    status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST']) 
def create_profile(request, user_id):
    return Response("done")
    