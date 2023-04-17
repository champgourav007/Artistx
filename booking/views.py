from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes

from auth_app.models import ArtistsProfile, Profile
from auth_app.views import create_response
from booking.models import Availability
from booking.serializers import AvailabilityRequestSerailizer, AvailabilityResponseSerializer
from constants.common.get_logged_user_profile import get_logged_user

@api_view(["GET","POST"])
@permission_classes([permissions.IsAuthenticated])
def get_unavailable_dates_for_artist(request):
  if request.method == 'POST':
    try:
      user = get_logged_user(request)
      profile = Profile.objects.get(user=user)
      artist = ArtistsProfile.objects.get(profile=profile)
      if artist:
        data = request.data
        data["artist"] = artist.pk
        serializer = AvailabilityRequestSerailizer(data=data)
        if serializer.is_valid():
          serializer.save()
          return Response(data=create_response('Data saved successfully.', status.HTTP_200_OK, None), status=status.HTTP_200_OK)
        else:
          return Response(data=create_response('Error Occured.', status.HTTP_204_NO_CONTENT, serializer.errors), status=status.HTTP_204_NO_CONTENT)
    except:
      return Response(data=create_response('You are not authorized.', status.HTTP_204_NO_CONTENT, None), status=status.HTTP_204_NO_CONTENT)
    
  if request.method == 'GET':
    try:
      profile_id = request.query_params.get('profile_id')
      artist = ArtistsProfile.objects.get(profile=profile_id)
      if artist:
        serializer = AvailabilityResponseSerializer(Availability.objects.get(artist_id=artist.id))
        return Response(data=create_response('Data fetched successfully.', status.HTTP_200_OK, serializer.data), status=status.HTTP_200_OK)
    except:
      return Response(data=create_response('You are not authorized.', status.HTTP_204_NO_CONTENT, None), status=status.HTTP_204_NO_CONTENT)