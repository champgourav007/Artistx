from django.urls import path

from booking import views

urlpatterns = [
  path('artist/calendar', views.get_unavailable_dates_for_artist, name='calendar'),
]