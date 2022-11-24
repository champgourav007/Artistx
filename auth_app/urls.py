from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('create_profile/<str:profile_id>', views.create_profile, name='create_profile'),
    path('activate_account/<str:profile_id>', views.activate_account, name='activate_account'),
    path('upload_profile_pic/<str:profile_id>', views.upload_profile_pic, name='upload_profile_pic'),
    path('login/', views.login_user, name='login'),
    path('send_email/', views.send_email, name='send_email'),
]
