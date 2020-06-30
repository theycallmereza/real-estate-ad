from django.contrib import admin
from .models import Category, Advertising, Property, Image, PropAd

# Register your models here.
admin.site.register(Category)
admin.site.register(Advertising)
admin.site.register(Property)
admin.site.register(Image)
admin.site.register(PropAd)