from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('create_profile/<str:profile_id>', views.create_profile, name='create_profile'),
    path('activate_account/<str:profile_id>', views.activate_account, name='activate_account'),
]
