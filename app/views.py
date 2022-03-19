from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.decorators import has_neighbourhood

from app.forms import ProfileForm
from app.models import Location, NeighbourHood

# Create your views here.


@login_required()
@has_neighbourhood
def index(request):
    return render(request, 'index.html')


@login_required()
def profile(request):
    title = f'Profile {request.user.full_name}'
    hoods = NeighbourHood.get_all_hoods()
    locations = Location.get_all_hoods()
    return render(request, 'profile.html', {'title': title, 'hoods': hoods, 'locations': locations})


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
