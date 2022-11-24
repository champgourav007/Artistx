from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)
from .serializers import (
    SignUpRequestSerailizer, 
    SignUpResponseSerailizer, 
    ProfileSerializer, 
    ProfilePicSerializer,
    UserSerializer
)
from .models import Profile, ArtistsProfile
from . import helpers
from django.template.loader import render_to_string
from artistx import settings
from .models import Profile
from .serializers import ProfileSerializer
from django.core.mail import EmailMessage
from django.conf import settings

DOMAIN = settings.ALLOWED_HOSTS_URI

def create_response(message, status, data):
    return {
    'message' : message,
    'status' : status,
    'data' : data
    }
    


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


# =================================Signup=================================
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
                'is_artist' : serializer.data.get('is_artist'),
            })
            
            if response.is_valid():
                # sending email is not working right now
                # sms_sent = send_email(user.email, profile.id, "Activate Account", "some")
                return Response(data=create_response('Successfully Created', status.HTTP_201_CREATED, response.data),
                                status=status.HTTP_201_CREATED)
            else:
                return Response(data=create_response(response.error_messages, status.HTTP_503_SERVICE_UNAVAILABLE, None), 
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
                            
        except:
            return Response(data=create_response('User Already Exists', status.HTTP_208_ALREADY_REPORTED, None),
                status=status.HTTP_208_ALREADY_REPORTED)
        
    return Response(data=create_response(serializer.error_messages , status.HTTP_400_BAD_REQUEST, None),
                    status=status.HTTP_400_BAD_REQUEST)

# =================================Activate Account=================================
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def activate_account(request, profile_id):
    profile_user = Profile.objects.get(id = profile_id)
    if profile_user:
        profile_user.is_email_verified = True
        profile_user.save()
        return Response(data=create_response('Account Activated Successfully', status.HTTP_202_ACCEPTED, None),
                        status=status.HTTP_202_ACCEPTED)
    else:
        Response(data=create_response('User does not exists or deleted.', status.HTTP_400_BAD_REQUEST, None),
                        status=status.HTTP_400_BAD_REQUEST)

# =================================Create Profile=================================
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_profile(request, profile_id):
    profile_user = Profile.objects.get(id = profile_id)
    if profile_user:
        if profile_user.is_email_verified:
            profile = ProfileSerializer(data=request.data)
            if profile.is_valid():
                data = profile.data
                profile_user.dob = data.get('dob', None) or profile_user.dob
                profile_user.country = data.get('country', None) or profile_user.country
                profile_user.state = data.get('state', None) or profile_user.state
                profile_user.currency_code = data.get('currency_code', None) or profile_user.currency_code
                profile_user.profile_headline = data.get('profile_headline', None) or profile_user.profile_headline
                profile_user.description = data.get('description', None) or profile_user.description
                profile_user.phone_number = data.get('phone_number', None) or profile_user.phone_number 
                profile_user.save()

                return Response(data=create_response('Account Updated Successfully', status.HTTP_201_CREATED, data),
                                status=status.HTTP_201_CREATED)
            else:
                return Response(data=create_response(profile.error_messages, status.HTTP_400_BAD_REQUEST, None),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=create_response(profile_user + ' is not Activated. Please activate your account.', status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, None),
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    else:
        return Response(data=create_response('User does not exists or deleted.', status.HTTP_400_BAD_REQUEST, None),
                        status=status.HTTP_400_BAD_REQUEST)

# =================================Upload Profile Pic=================================
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_profile_pic(request, profile_id):
    profile_user = Profile.objects.get(id = profile_id)
    if profile_user:
        profile_photo = request.FILES['profile_photo']
        profile_user.profile_photo = profile_photo
        profile_user.save()
        return Response(data=create_response('Profile Image Updated Successfully', status.HTTP_201_CREATED, None),
                        status=status.HTTP_201_CREATED)  
    else:
        return Response(data=create_response('User Does not Exists', status.HTTP_404_NOT_FOUND, None),
                        status=status.HTTP_404_NOT_FOUND)

# =================================Login=================================
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username, password = request.data.get('username'), request.data.get('password')
    user = User.objects.get(email = username)
    if user:
        profile = Profile.objects.get(user_id = user.id)
        if profile.is_email_verified:    
            if user.check_password(password):
                login(request, user)
                tokens = get_tokens_for_user(user)
                return Response(data=create_response("Login Successfull", status.HTTP_202_ACCEPTED, {
                    "access_token" : tokens['access'],
                    "refresh_token" : tokens['refresh'],
                    "user_details" : UserSerializer(user).data,
                    "profile_details" : ProfileSerializer(profile).data,
                }),
                                status=status.HTTP_202_ACCEPTED)
            else:
                return Response(data=create_response("Password does not matched.", status.HTTP_200_OK, None),
                                status=status.HTTP_200_OK)
        else:
            Response(data=create_response("Please Verify your Email", status.HTTP_200_OK, None),
                     status=status.HTTP_200_OK)
    else:
        return Response(data=create_response("User Does not Exists.", status.HTTP_400_BAD_REQUEST, None),
                        status=status.HTTP_400_BAD_REQUEST)
    
# =================================Logout=================================
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    try:
        logout(request)
        return Response(data=create_response('Logout Successfully', status.HTTP_200_OK, None),
                        status=status.HTTP_200_OK)
    except:
        return Response(data=create_response('Logout Successfully', status.HTTP_401_UNAUTHORIZED, None),
                        status=status.HTTP_401_UNAUTHORIZED)

# =================================Forgot Password=================================
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def forgot_password(request):
    user = User.objects.get(email = request.data.get('email'))
    if user:
        pass
    else:
        return Response(data=create_response('User does not exists. Please check emai id.', status.HTTP_404_NOT_FOUND, None),
                        status=status.HTTP_404_NOT_FOUND)
        
# =================================Send Email=================================
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_email(request):
    data = request.data
    profile_id, subject, email = data.get('profile_id'), data.get('subject'), data.get('email')
    message = render_to_string(
        'auth_app/email.html',
        context={
            "domain" : DOMAIN,
            "profile_id" : profile_id,
        }
    )
    email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )

    email.fail_silently = False
    email.send()
    return Response("Account Activated")