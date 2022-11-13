from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('create_profile/<int:user_id>', views.create_profile, name='create_profile'),
]
