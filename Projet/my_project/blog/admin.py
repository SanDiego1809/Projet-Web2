from django.contrib import admin
from .models import Post, Watchlist

# Register your models here.
admin.site.register(Post)
admin.site.register(Watchlist)