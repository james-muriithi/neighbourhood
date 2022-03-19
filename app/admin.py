from django.contrib import admin

from app.models import Business, Contact, Location, NeighbourHood, Post, User


class NeighbourHoodAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class BusinessAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


# Register your models here.
admin.site.register(User)
admin.site.register(NeighbourHood, NeighbourHoodAdmin)
admin.site.register(Location)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Contact)
admin.site.register(Post, PostAdmin)
