from django.urls import path

from . import views

urlpatterns = [
    path('get-user/<int:user_id>', views.get_user, name='get-user'),
    path('get-sorted-artists/', views.sort_artists_using_db_column, name='sort_artists_using_db_column'),
]
