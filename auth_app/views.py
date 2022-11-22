from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)
from .serializers import SignUpRequestSerailizer, SignUpResponseSerailizer
from .models import Profile

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    '''Function for signup'''
    serializer = SignUpRequestSerailizer(data=request.data)
    
    if serializer.is_valid():
        try:
            user = User.objects.create_user(
                username = serializer.data.get('email'),
                first_name = serializer.data.get('first_name'),
                last_name = serializer.data.get('last_name'),
                email = serializer.data.get('email'),
                password = serializer.data.get('password'),
            )
            user.is_active = True
            user.save()
            
            profile = Profile.objects.create(
                user = user,
                dob = serializer.data.get('dob'),
            )
            profile.save()
            tokens = get_tokens_for_user(user)
            response = SignUpResponseSerailizer(data={
                'first_name' : serializer.data.get('first_name'),
                'last_name' : serializer.data.get('last_name'),
                'email' : serializer.data.get('email'),
                'dob' : serializer.data.get('dob'),
                'profile_id' : profile.id,
                'access_token' : tokens.get('access'),
                'refresh_token' : tokens.get('refresh'),
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
@permission_classes([permissions.IsAuthenticated])
def create_profile(request, user_id):
    return Response("done")
    