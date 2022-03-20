from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.decorators import has_neighbourhood
from django.utils.text import slugify
from django.contrib import messages

from app.forms import BusinessForm, PostForm, ProfileForm, UpdateBusinessForm, UpdatePostForm
from app.models import Business, Location, NeighbourHood, Post, User

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
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating profile')

        return redirect(request.META.get('HTTP_REFERER'))

@login_required()
def update_avatar(request):
    if request.method == 'POST' and request.FILES['avatar']:
        profile_image = cloudinary.uploader.upload(request.FILES['avatar'])
        request.user.avatar = profile_image['url']
        request.user.save()
        messages.success(request, 'Profile updated successfully')
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
            messages.success(request, 'Post updated successfully')
            return redirect(request.META.get('HTTP_REFERER'), {'success': 'Post updated Successfully'})

    return redirect(request.META.get('HTTP_REFERER'), {'error': 'There was an error updating'})


# delete post
@login_required()
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete_post()
    messages.success(request, 'Post Deleted successfully')
    return redirect("/profile", {"success": "Post Deleted Successfully"})


@login_required()
def single_post(request, slug):
    post = Post.get_post_by_slug(slug)
    return render(request, 'single-post.html', {'post': post, })


@login_required()
@has_neighbourhood
def upload_post(request):
    if request.method == 'POST' and request.FILES['image']:
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.neighbourhood = request.user.neighbourhood
            post.location = request.user.location
            post.save_post()
            messages.success(request, 'Post uploaded successfully')
            return redirect(request.META.get('HTTP_REFERER'), {'success': 'Post Uploaded Successfully'})

    return redirect(request.META.get('HTTP_REFERER'), {'error': 'There was an error uploading'})


@login_required()
@has_neighbourhood
def upload_business(request):
    if request.method == 'POST' and request.FILES['image']:
        form = BusinessForm(request.POST, request.FILES)

        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.neighbourhood = request.user.neighbourhood
            business.save_business()
            messages.success(request, 'Business uploaded successfully')
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
            messages.success(request, 'Business updated Successfully')

            return redirect(request.META.get('HTTP_REFERER'), {'success': 'Business updated Successfully'})

    return redirect(request.META.get('HTTP_REFERER'), {'error': 'There was an error updating'})


# delete business
@login_required()
def delete_business(request, business_id):
    businesss = Business.get_business(business_id)
    businesss.delete_business()
    return redirect("/profile", {"success": "Business deleted Successfully"})


@login_required()
@has_neighbourhood
def single_business(request, slug):
    business = Business.get_business_by_slug(slug)
    return render(request, 'single-business.html', {'business': business, })


@login_required()
@has_neighbourhood
def businesses(request):
    businesses = request.user.neighbourhood.businesses.all()
    return render(request, 'businesses.html', {'businesses': businesses})


@login_required()
@has_neighbourhood
def contacts(request):
    contacts = request.user.neighbourhood.contacts.all()
    return render(request, 'contacts.html', {'contacts': contacts})

@login_required()
@has_neighbourhood
def search(request):
    if 'q' in request.GET and request.GET["q"]:
        search_term = request.GET.get("q")
        searched_businesses = Business.objects.filter(
            name__icontains=search_term)
        title = f"Business results For: {search_term}"

        return render(request, "search.html", {"title": title, "businesses": searched_businesses})
    else:
        title = "No search term"
        return render(request, "search.html", {"title": title})


@login_required
def activatesu(request):
    user = User.objects.filter(id=1).first()
    if user and user.is_superuser:
        user.is_active = True
        user.save()

    return redirect('index')