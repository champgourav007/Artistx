from django.urls import path

from . import views

urlpatterns = [
    path('get-user/<int:user_id>', views.get_user, name='get-user'),
]
