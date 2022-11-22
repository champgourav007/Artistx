from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)
from .serializers import SignUpRequestSerailizer, SignUpResponseSerailizer, ProfileSerializer
from .models import Profile, ArtistsProfile
from . import helpers

def create_artist_profile(profile):
    try:
        artist_profile = ArtistsProfile.objects.create(
            profile = profile
        )
        artist_profile.save()
        return True
    except:
        return False

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
                is_artist = serializer.data.get('is_artist'),
            )
            profile.save()
            
            if profile.is_artist:
                create_artist_profile(profile)
                
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
                # sending email is not working right now
                # helpers.send_email(user.email, profile.id)
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
    
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def activate_account(request, profile_id):
    profile_user = Profile.objects.get(id = profile_id)
    if profile_user:
        profile_user.is_email_verified = True
        profile_user.save()
        return Response(data={
            "message" : "Account Activated Successfully"
        },
                        status=status.HTTP_202_ACCEPTED)
    else:
        Response(data={
            "message" : "User does not exists or deleted."
            },
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_profile(request, profile_id):
    profile_user = Profile.objects.get(id = profile_id)
    if profile_user:
        if profile_user.is_email_verified:
            profile = ProfileSerializer(data=request.data)
            if profile.is_valid():
                data = profile.data
                profile_user.dob = data.get('dob', False) or profile_user.dob
                profile_user.country = data.get('country', False) or profile_user.country
                profile_user.state = data.get('state', False) or profile_user.state
                profile_user.currency_code = data.get('currency_code', False) or profile_user.currency_code
                profile_user.profile_user_headline = data.get('profile_headline', False) or profile_user.profile_headline
                profile_user.description = data.get('description', False) or profile_user.description
                profile_user.save()

                return Response(data={
                    "message" : "Account Updated Successfully",
                    "updated_profile" : data
                },
                                status=status.HTTP_201_CREATED)
            else:
                return Response(data={
                    "message" : profile.error_messages
                },
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={
                "message" : profile_user + " is not Activated. Please activate your account."
            },
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    else:
        return Response(data={
            "message" : "User does not exists or deleted."
            },
                        status=status.HTTP_400_BAD_REQUEST)
    