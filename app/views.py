from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.decorators import has_neighbourhood
from django.utils.text import slugify

from app.forms import BusinessForm, PostForm, ProfileForm, UpdateBusinessForm, UpdatePostForm
from app.models import Business, Location, NeighbourHood, Post

# Create your views here.


@login_required()
@has_neighbourhood
def index(request):
    posts = Post.get_all_posts()
    return render(request, 'index.html', {'posts': posts})


@login_required()
def profile(request):
    title = f'Profile {request.user.full_name}'
    hoods = NeighbourHood.get_all_hoods()
    locations = Location.get_all_locations()
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


@login_required()
def update_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        form = UpdatePostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            return redirect(request.META.get('HTTP_REFERER'), {'success': 'Post updated Successfully'})

    return redirect(request.META.get('HTTP_REFERER'), {'error': 'There was an error updating'})


# delete post
@login_required()
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete_post()
    return redirect("/profile", {"success": "Post Deleted Successfully"})


@login_required()
def single_post(request, slug):
    post = Post.get_post_by_slug(slug)
    return render(request, 'single-post.html', {'post': post, })


@login_required()
def upload_post(request):
    if request.method == 'POST' and request.FILES['image']:
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.neighbourhood = request.user.neighbourhood
            post.location = request.user.location
            post.save_post()

            return redirect(request.META.get('HTTP_REFERER'), {'success': 'Post Uploaded Successfully'})

    return redirect(request.META.get('HTTP_REFERER'), {'error': 'There was an error uploading'})


@login_required()
def upload_business(request):
    if request.method == 'POST' and request.FILES['image']:
        form = BusinessForm(request.POST, request.FILES)

        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.neighbourhood = request.user.neighbourhood
            business.save_business()

            return redirect(request.META.get('HTTP_REFERER'), {'success': 'Business Uploaded Successfully'})

    return redirect(request.META.get('HTTP_REFERER'), {'error': 'There was an error uploading'})


@login_required()
def update_business(request, business_id):
    if request.method == 'POST':
        business = Business.get_business(business_id)
        form = UpdateBusinessForm(request.POST, instance=business)

        if form.is_valid():
            business = form.save(commit=False)
            business.slug = slugify(business.name)
            business.save()
            return redirect(request.META.get('HTTP_REFERER'), {'success': 'Business updated Successfully'})

    return redirect(request.META.get('HTTP_REFERER'), {'error': 'There was an error updating'})


# delete business
@login_required()
def delete_business(request, business_id):
    businesss = Business.get_business(business_id)
    businesss.delete_business()
    return redirect("/profile", {"success": "Business deleted Successfully"})


@login_required()
def single_business(request, slug):
    business = Business.get_business_by_slug(slug)
    return render(request, 'single-business.html', {'business': business, })
