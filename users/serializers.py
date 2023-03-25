import sys
sys.path.append('..')
from rest_framework import serializers
from django.contrib.auth.models import User
from constants.users import FiltersConstants as constants

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ('password',)
    
class FiltersListSerializers(serializers.Serializer):
  location = serializers.CharField(max_length=255)


class FilterArtistSerializer(serializers.Serializer):
  profile_id = serializers.UUIDField()
  first_name = serializers.CharField(max_length=255)
  last_name = serializers.CharField(max_length=255)
  genre = serializers.ChoiceField(choices=constants.GENRE)
  description = serializers.CharField(max_length=255)
  state = serializers.CharField(max_length=255)
  country = serializers.CharField(max_length=255)
  rating = serializers.DecimalField(decimal_places=1, max_digits=10)
  profile_photo = serializers.EmailField()
  profile_photo_thumb = serializers.EmailField()
  
  