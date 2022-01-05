from django.contrib import admin
from .models import User, Category, Music, Movie
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Music)
admin.site.register(Movie)
