from django.contrib import admin
from .models import Video,Category,Comment,Like,WatchLater
admin.site.register([Video,Category,Comment,Like,WatchLater])
