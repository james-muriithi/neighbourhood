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

    @classmethod
    def get_location(cls, id):
        return cls.objects.get(id=id)

    def __str__(self):
        return self.name


# NeighbourHood Model
class NeighbourHood(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(null=True, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    admin = models.ForeignKey(
        'app.User', on_delete=models.CASCADE, related_name='neighbourhoods', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def create_neigborhood(self):
        self.slug = slugify(self.name)
        self.save()

    def delete_neighbourhood(self):
        self.delete()

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

    class Meta:
        ordering = ['-created_at']


class Business(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=True, unique=True)
    image = CloudinaryField('image', blank=True, null=True)
    email = models.EmailField(max_length=150)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        'app.User', on_delete=models.CASCADE, related_name="businesses", null=True)
    neighbourhood = models.ForeignKey(
        NeighbourHood, on_delete=models.CASCADE, related_name="businesses", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def thumbnail(self):
        return self.image.build_url(height=200, crop="pad", format='webp')

    @property
    def business_image(self):
        return self.image.build_url(format='webp')

    # create business
    def save_business(self):
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

    # find business by slug
    @classmethod
    def get_business_by_slug(cls, slug):
        business = cls.objects.get(slug=slug)
        return business

    @classmethod
    def get_all_businesses(cls):
        return cls.objects.all()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50)
    neighbourhood = models.ForeignKey(
        NeighbourHood, on_delete=models.CASCADE, related_name="contacts", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # create contact
    def create_contact(self):
        self.save()

    @classmethod
    def get_contact(cls, id):
        return cls.objects.get(id=id)

    def __str__(self):
        return self.name


# post class model
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True, unique=True)
    content = models.TextField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    user = models.ForeignKey(
        'app.User', on_delete=models.CASCADE, related_name='posts', null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    neighbourhood = models.ForeignKey(
        NeighbourHood, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def thumbnail(self):
        return self.image.build_url(height=200, crop="pad", format='webp')

    @property
    def post_image(self):
        return self.image.build_url(format='webp')

    # save post
    def save_post(self):
        self.slug = slugify(self.title)
        self.save()

    # delete post
    def delete_post(self):
        self.delete()

    # update post
    def update_post(self):
        self.update()

    @classmethod
    def get_post_by_slug(cls, slug):
        return cls.objects.get(slug=slug)

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

    @classmethod
    def get_all_posts(cls):
        return cls.objects.all()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class User(AbstractUser):
    full_name = models.CharField(max_length=124)
    email = models.CharField(max_length=124, unique=True)
    avatar = CloudinaryField('image', null=True)
    bio = models.TextField(max_length=500, null=True)
    contact = models.TextField(max_length=20, null=True,)
    neighbourhood = models.ForeignKey(
        NeighbourHood, on_delete=models.SET_NULL, null=True, related_name="users",)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    @property
    def url_formatted_name(self):
        return self.full_name.replace(' ', '+') or self.username

    @property
    def user_avatar(self):
        return self.avatar if self.avatar else f'https://ui-avatars.com/api/?name={self.url_formatted_name}&background=49c5b6&color=fff'
