from django.contrib import admin
from .models import Post, Watchlist, Messages

# Register your models here.
admin.site.register(Post)
admin.site.register(Watchlist)
admin.site.register(Messages)
