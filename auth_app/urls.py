from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('update_profile/<str:profile_id>', views.update_profile, name='update_profile'),
    path('activate_account/<str:profile_id>', views.activate_account, name='activate_account'),
    path('upload_profile_pic/<str:profile_id>', views.upload_profile_pic, name='upload_profile_pic'),
    path('login/', views.login_user, name='login'),
    path('send_email/', views.send_email, name='send_email'),
    path('update_artist_profile/<str:profile_id>', views.update_artist_profile, name='update_artist_profile'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]
