import sys
sys.path.append('..')
from rest_framework import serializers
from django.contrib.auth.models import User
from constants.users import FiltersConstants as constants

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ('password',)
    
class FiltersListSerializers(serializers.BaseSerializer):
  location = serializers.CharField(max_length=255)
