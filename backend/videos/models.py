from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
 name=models.CharField(max_length=80,unique=True)
 slug=models.SlugField(unique=True)
 def __str__(self):return self.name
class Video(models.Model):
 title=models.CharField(max_length=200)
 description=models.TextField(blank=True)
 video_file=models.FileField(upload_to='videos/')
 thumbnail=models.ImageField(upload_to='thumbnails/',blank=True,null=True)
 category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='videos')
 uploaded_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='videos')
 uploaded_at=models.DateTimeField(auto_now_add=True)
 views=models.PositiveIntegerField(default=0)
 def __str__(self):return self.title
class Comment(models.Model):
 video=models.ForeignKey(Video,on_delete=models.CASCADE,related_name='comments')
 user=models.ForeignKey(User,on_delete=models.CASCADE)
 text=models.TextField(max_length=2000)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:ordering=['-created_at']
class Like(models.Model):
 video=models.ForeignKey(Video,on_delete=models.CASCADE,related_name='likes')
 user=models.ForeignKey(User,on_delete=models.CASCADE)
 class Meta:constraints=[models.UniqueConstraint(fields=['video','user'],name='unique_video_like')]
class WatchLater(models.Model):
 video=models.ForeignKey(Video,on_delete=models.CASCADE)
 user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='saved_videos')
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:constraints=[models.UniqueConstraint(fields=['video','user'],name='unique_saved_video')];ordering=['-created_at']
