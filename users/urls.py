from django.urls import path

from . import views

urlpatterns = [
    path('get-user/<int:user_id>', views.get_user, name='get-user'),
    path('get-sorted-artists/', views.sort_artists_using_db_column, name='sort-artists-using-db-column'),
    path('get-artist-by-search-term/', views.get_artist_by_search_term, name='get-artist-by-search-term'),
    path('get-filters-list/', views.get_filters_list, name='get-filters-list'),
]
