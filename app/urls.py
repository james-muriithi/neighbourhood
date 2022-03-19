from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('profile', views.profile, name="profile"),
    path('update_profile', views.update_profile, name="update_profile"),
    path('update_avatar', views.update_avatar, name="update_avatar"),
]
