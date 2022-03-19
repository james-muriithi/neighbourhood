from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


# Create your models here.
# location model
class Location(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    # save location
    def save_location(self):
        self.save()

    @classmethod
    def get_all_locations(cls):
        return cls.objects.all()

    def __str__(self):
        return self.name


# NeighbourHood Model
class NeighbourHood(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(null=True, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    admin = models.ForeignKey(
        'app.User', on_delete=models.CASCADE, related_name='neighbourhoods')
    created_at = models.DateTimeField(auto_now_add=True)

    def create_neigborhood(self):
        self.slug = slugify(self.name)
        self.save()

    @classmethod
    def delete_neighbourhood(cls, id):
        cls.objects.filter(id=id).delete()

    @classmethod
    def update_neighbourhood(cls, id):
        cls.objects.filter(id=id).update()

    @classmethod
    def search_by_name(cls, search_term):
        hood = cls.objects.filter(name__icontains=search_term)
        return hood

    # find neighbourhood by id
    @classmethod
    def find_neigborhood(cls, id):
        hood = cls.objects.get(id=id)
        return hood

    # find neighbourhood by slug
    @classmethod
    def find_neigborhood_by_slug(cls, slug):
        return cls.objects.get(slug=slug)

    @classmethod
    def get_all_hoods(cls):
        hoods = cls.objects.all()
        return hoods

    def __str__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=True, unique=True)
    email = models.EmailField(max_length=150)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey('app.User', on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # create business
    def create_business(self):
        self.slug = slugify(self.name)
        self.save()

    # delete business
    def delete_business(self):
        self.delete()

    # update business
    def update_business(self):
        self.update()

    # search business
    @classmethod
    def search_business(cls, search_term):
        business = cls.objects.filter(name__icontains=search_term)
        return business

    # find business by id
    @classmethod
    def get_business(cls, id):
        business = cls.objects.get(id=id)
        return business

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # create contact
    def create_contact(self):
        self.save()

    def __str__(self):
        return self.name


# post class model
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    user = models.ForeignKey('app.User', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # create post
    def create_post(self):
        self.save()

    # delete post
    def delete_post(self):
        self.delete()

    # update post
    def update_post(self):
        self.update()

    # search post
    @classmethod
    def search_by_title(cls, search_term):
        post = cls.objects.filter(title__icontains=search_term)
        return post

    # find post by id
    @classmethod
    def find_post(cls, id):
        post = cls.objects.get(id=id)
        return post

    def __str__(self):
        return self.title


class User(AbstractUser):
    full_name = models.CharField(max_length=124)
    email = models.CharField(max_length=124, unique=True)
    avatar = CloudinaryField('image', null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    contact = models.TextField(max_length=20, blank=True, null=True)
    neighbourhood = models.ForeignKey(
        NeighbourHood, on_delete=models.SET_NULL, null=True, related_name="users")
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    @property
    def url_formatted_name(self):
        return self.full_name.replace(' ', '+') or self.username

    @property
    def user_avatar(self):
        return self.avatar if self.avatar else f'https://ui-avatars.com/api/?name={self.url_formatted_name}&background=49c5b6&color=fff'
