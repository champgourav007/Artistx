import json
from rest_framework import serializers
from django.db.models import F
from booking.models import Availability, Dates, WeekDays

from constants.booking.availability_choices import AVAILABILITY_CHOICES


class DatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dates
        exclude = ('availability','id')

class WeekDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekDays
        exclude = ('availability', 'id')

class AvailabilityRequestSerailizer(serializers.ModelSerializer):
    dates = DatesSerializer(many=True)
    week_days = WeekDaysSerializer(many=True)
    class Meta:
        model = Availability
        fields = ("__all__")
        
    def create(self, validated_data):
        dates_data = validated_data.pop('dates')
        week_days_data = validated_data.pop('week_days')
        availability = Availability.objects.create(**validated_data)
        for week_day in week_days_data:
            WeekDays.objects.create(availability=availability, **week_day)
        for date in dates_data:
            Dates.objects.create(availability=availability,**date)
        return availability
    
    # def update(self, validated_data):
    #     dates_data = validated_data.pop('dates')
    #     week_days_data = validated_data.pop('week_days')
    #     availability = Availability.objects.update(**validated_data)
    #     for week_day in week_days_data:
    #         WeekDays.objects.update(availability=availability, **week_day)
    #     for date in dates_data:
    #         Dates.objects.update(availability=availability,**date)
    #     return availability
    
class AvailabilityResponseSerializer(serializers.ModelSerializer):
    dates = serializers.SerializerMethodField()
    week_days = serializers.SerializerMethodField()
    
    def get_dates(self, obj):
        queryset = Dates.objects.filter(availability=obj)
        return DatesSerializer(queryset, many=True).data
        
    def get_week_days(self, obj):
        queryset = WeekDays.objects.filter(availability=obj)
        return WeekDaysSerializer(queryset, many=True).data
        
    class Meta:
        model = Availability
        exclude = ("artist", "id")