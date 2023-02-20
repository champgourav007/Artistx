from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes

from users.serializers import UserSerializer

from auth_app.serializers import (
  ProfileSerializer,
  ArtistProfileSerializer,
  LanguagesSerializer
)
from auth_app.models import (
  ArtistsProfile,
  Profile,
  Language
)
from auth_app.views import create_response
from drf_yasg.utils import swagger_auto_schema

import requests


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user(request, user_id):
  try:
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    languages = Language.objects.filter(profile=profile)
    artist_profile = None
    if profile.is_artist:
      artist_profile = ArtistsProfile.objects.get(profile=profile)
  except:
    return Response(create_response('Please check the id.', status.HTTP_400_BAD_REQUEST, None),
                    status=status.HTTP_400_BAD_REQUEST)
  if user:
    user_data = UserSerializer(user).data
    profile_data = ProfileSerializer(profile).data
    languages = LanguagesSerializer(languages, many=True).data
    artist_profile_data = None
    if artist_profile:
      artist_profile_data = ArtistProfileSerializer(artist_profile).data
      
    return Response(create_response('Successfull Response', status.HTTP_200_OK, {
                    "user_details" : user_data,
                    "languages" : languages,
                    "profile_details" : profile_data,
                    "artist_details" : artist_profile_data,
      }),
                    status=status.HTTP_200_OK)
  else:
    return Response(create_response("serailizer.error_messages", status.HTTP_400_BAD_REQUEST, None),
                    status=status.HTTP_400_BAD_REQUEST)
    
# to be done
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def sort_artists_using_db_column(request):
  col, sort_dir  = request.query_params.get('col'), request.query_params.get('sortDir')
  if col.lower() == 'genre':
    artists = ArtistsProfile.objects.order_by(str(col))
    print(artists)
  return Response("Dne")


# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def sort_artists_using_location(request, lat, lng):
