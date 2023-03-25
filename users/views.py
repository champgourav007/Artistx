import json
import sys
from django.http import JsonResponse
sys.path.append("..")
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q, F
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes

from users.serializers import (
  FilterArtistSerializer,
  UserSerializer,
  FiltersListSerializers
)

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

from constants.users import FiltersConstants as constants

def get_artist_profile(userModel:User=None, profileModel:Profile=None, artistModel:ArtistsProfile=None):
  try:
    if userModel:
      user = userModel
      profile = Profile.objects.get(user=userModel)
      artist = ArtistsProfile.objects.get(profile=profile)
      
    if profileModel:
      user = User.objects.get(pk=profileModel.user_id)
      artist = ArtistsProfile.objects.get(profile=profileModel)
      profile = profileModel
      
    if artistModel:
      profile = Profile.objects.get(pk=artistModel.profile_id)
      user = User.objects.get(pk=profile.user_id)
      artist = artistModel
      
    if not artist:
      return None
    
    return {
      'profile_id' : profile.id,
      'first_name' : user.first_name,
      'last_name' : user.last_name,
      'genre' : artist.genre,
      'description' : profile.description,
      'rating' : artist.rating,
      'state' : profile.state,
      'country' : profile.country,
      'profile_photo' : profile.profile_photo,
      'profile_photo_thumb' : profile.profile_photo_thumb
    }
  except:
    return None
    

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
    return Response(data=create_response('Please check the id.', status.HTTP_400_BAD_REQUEST, None),
                    status=status.HTTP_400_BAD_REQUEST)
  if user:
    user_data = UserSerializer(user).data
    profile_data = ProfileSerializer(profile).data
    languages = LanguagesSerializer(languages, many=True).data
    artist_profile_data = None
    if artist_profile:
      artist_profile_data = ArtistProfileSerializer(artist_profile).data
      
    return Response(data=create_response('Successfull Response', status.HTTP_200_OK, {
                    "user_details" : user_data,
                    "languages" : languages,
                    "profile_details" : profile_data,
                    "artist_details" : artist_profile_data,
      }),
                    status=status.HTTP_200_OK)
  else:
    return Response(data=create_response("serailizer.error_messages", status.HTTP_400_BAD_REQUEST, None),
                    status=status.HTTP_400_BAD_REQUEST)

# to be done
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def sort_artists_using_db_column(request):
  col, sort_dir  = request.query_params.get('col'), request.query_params.get('sortDir')
  if col.lower() == 'genre':
    artists = ArtistsProfile.objects.order_by(str(col))
    print(artists)
  return Response("Done")


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_filters_list(request):
  return Response(data=create_response(
    'Successful Response', status.HTTP_200_OK, {
      'Location' : constants.LOCATIONS,
      'Genre' : constants.GENRE,
      'Rating' : constants.RATING
    }
  ),
                  status=status.HTTP_200_OK)

# =================================Get Artist By Search Term=================================
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_artist_by_search_term(request):
  try:
    
    params = request.query_params
    search_term, rating, location, genre =  params.get('search_term'), params.get('rating'), params.get('location'), params.get('genre')
    data_dict = {}
    artists_list = []
    
    rating = rating if rating else 5

    if search_term:
      res_name = User.objects.filter(Q(first_name__contains=search_term) | Q(last_name__contains=search_term))
      for user in res_name:
        user_profile = get_artist_profile(user, None, None)
        if user_profile and not data_dict.get(user_profile.get('profile_id')):
          artists_list.append(FilterArtistSerializer(user_profile).data)
          data_dict[user_profile.get('profile_id')] = 1
    
    if rating:
      res_rating = ArtistsProfile.objects.filter(rating=rating)
      for rat in res_rating:
        rating_profile = get_artist_profile(None, None, rat)
        if rating_profile and not data_dict.get(rating_profile.get('profile_id')):
          artists_list.append(FilterArtistSerializer(rating_profile).data)
          data_dict[rating_profile.get('profile_id')] = 1
    
    if location:
      res_location = Profile.objects.filter(state=location)
      for loc in res_location:
        location_profile = get_artist_profile(None, loc, None)
        if location_profile and not data_dict.get(location_profile.get('profile_id')):
          artists_list.append(FilterArtistSerializer(location_profile).data)
          data_dict[location_profile.get('profile_id')] = 1
    
    if genre:
      res_genre = ArtistsProfile.objects.filter(genre=genre)
      for gen in res_genre:
        genre_profile = get_artist_profile(None, None, gen)
        if genre_profile and not data_dict.get(genre_profile.get('profile_id')):
          artists_list.append(FilterArtistSerializer(genre_profile).data)
          data_dict[genre_profile.get('profile_id')] = 1

    return Response(data=create_response("Successfull Response", status.HTTP_200_OK, artists_list),
                    status=status.HTTP_200_OK)
  except:
    return Response(data=create_response("Something went wrong", status.HTTP_400_BAD_REQUEST, None),
                    status=status.HTTP_400_BAD_REQUEST)
