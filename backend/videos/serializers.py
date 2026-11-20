from rest_framework import serializers
from .models import Video,Category,Comment,WatchLater
class CategorySerializer(serializers.ModelSerializer):
 class Meta:model=Category;fields=['id','name','slug']
class VideoSerializer(serializers.ModelSerializer):
 creator=serializers.CharField(source='uploaded_by.username',read_only=True)
 category_name=serializers.CharField(source='category.name',read_only=True)
 likes_count=serializers.IntegerField(read_only=True)
 is_liked=serializers.BooleanField(read_only=True)
 is_saved=serializers.BooleanField(read_only=True)
 class Meta:
  model=Video;fields=['id','title','description','video_file','thumbnail','category','category_name','uploaded_by','creator','uploaded_at','views','likes_count','is_liked','is_saved'];read_only_fields=['uploaded_by','views','uploaded_at']
 def validate_video_file(self,file):
  if file.size>200*1024*1024:raise serializers.ValidationError('Maximum video size is 200 MB.')
  if not file.name.lower().endswith(('.mp4','.webm','.ogg')):raise serializers.ValidationError('Use MP4, WebM or OGG video.')
  return file
 def validate_thumbnail(self,file):
  if file and file.size>5*1024*1024:raise serializers.ValidationError('Thumbnail must be under 5 MB.')
  return file
class CommentSerializer(serializers.ModelSerializer):
 username=serializers.CharField(source='user.username',read_only=True)
 class Meta:model=Comment;fields=['id','video','user','username','text','created_at'];read_only_fields=['video','user','created_at']
class WatchLaterSerializer(serializers.ModelSerializer):
 video=VideoSerializer(read_only=True)
 class Meta:model=WatchLater;fields=['id','video','created_at']
