from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import cloudinary
import cloudinary.uploader
import cloudinary.api

from app.forms import ProfileForm

# Create your views here.


@login_required()
def index(request):
    return render(request, 'index.html')


@login_required()
def profile(request):
    title = f'Profile {request.user.full_name}'
    return render(request, 'profile.html', {'title': title})


@login_required()
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect(request.META.get('HTTP_REFERER'), {'success': 'Profile updated successfully'})


@login_required()
def update_avatar(request):
    if request.method == 'POST' and request.FILES['avatar']:
        profile_image = cloudinary.uploader.upload(request.FILES['avatar'])
        request.user.avatar = profile_image['url']
        request.user.save()
        return redirect(request.META.get('HTTP_REFERER'), {'success': 'Profile updated successfully'})
