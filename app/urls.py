from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('profile', views.profile, name="profile"),
    path('update_profile', views.update_profile, name="update_profile"),
    path('update_avatar', views.update_avatar, name="update_avatar"),
    path('post/<slug>', views.single_post, name="single_post"),
    path('post/<post_id>/delete', views.delete_post, name="post_delete"),
    path('post/<post_id>/update', views.update_post, name="update_post"),
    path('upload_post', views.upload_post, name='upload_post'),
    path('business/<slug>', views.single_business, name="single_business"),
    path('business/<business_id>/delete',
         views.delete_business, name="business_delete"),
    path('business/<business_id>/update',
         views.update_business, name="update_business"),
    path('upload_business', views.upload_business, name='upload_business'),
]
