from django.db.models import Count,Exists,OuterRef,F,Q
from django.shortcuts import get_object_or_404
from rest_framework import generics,permissions,status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Video,Category,Comment,Like,WatchLater
from .serializers import VideoSerializer,CategorySerializer,CommentSerializer,WatchLaterSerializer

def videos_for(request):
 qs=Video.objects.select_related('category','uploaded_by').annotate(likes_count=Count('likes',distinct=True))
 if request.user.is_authenticated:
  qs=qs.annotate(is_liked=Exists(Like.objects.filter(video=OuterRef('pk'),user=request.user)),is_saved=Exists(WatchLater.objects.filter(video=OuterRef('pk'),user=request.user)))
 else:qs=qs.annotate(is_liked=Exists(Like.objects.none()),is_saved=Exists(WatchLater.objects.none()))
 return qs
class VideoList(generics.ListAPIView):
 serializer_class=VideoSerializer
 def get_queryset(self):
  qs=videos_for(self.request)
  category=self.request.query_params.get('category')
  if category:qs=qs.filter(category__slug=category)
  return qs.order_by('-uploaded_at')
class VideoDetail(generics.RetrieveAPIView):
 serializer_class=VideoSerializer
 def get_queryset(self):return videos_for(self.request)
class UploadVideo(generics.CreateAPIView):
 permission_classes=[permissions.IsAuthenticated];serializer_class=VideoSerializer
 def perform_create(self,serializer):serializer.save(uploaded_by=self.request.user)
class MyVideos(generics.ListAPIView):
 permission_classes=[permissions.IsAuthenticated];serializer_class=VideoSerializer
 def get_queryset(self):return videos_for(self.request).filter(uploaded_by=self.request.user).order_by('-uploaded_at')
class SearchVideos(generics.ListAPIView):
 serializer_class=VideoSerializer
 def get_queryset(self):
  q=self.request.query_params.get('q','').strip()[:100]
  return videos_for(self.request).filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(category__name__icontains=q)).order_by('-uploaded_at') if q else Video.objects.none()
class Categories(generics.ListAPIView):
 queryset=Category.objects.all().order_by('name');serializer_class=CategorySerializer;pagination_class=None
class CategoryVideos(generics.ListAPIView):
 serializer_class=VideoSerializer
 def get_queryset(self):
  get_object_or_404(Category,pk=self.kwargs['pk'])
  return videos_for(self.request).filter(category_id=self.kwargs['pk']).order_by('-uploaded_at')
class Comments(generics.ListCreateAPIView):
 serializer_class=CommentSerializer;pagination_class=None
 def get_queryset(self):return Comment.objects.filter(video_id=self.kwargs['pk']).select_related('user')
 def get_permissions(self):return [permissions.IsAuthenticated()] if self.request.method=='POST' else [permissions.AllowAny()]
 def perform_create(self,serializer):serializer.save(user=self.request.user,video=get_object_or_404(Video,pk=self.kwargs['pk']))
class DeleteComment(generics.DestroyAPIView):
 permission_classes=[permissions.IsAuthenticated];serializer_class=CommentSerializer
 def get_queryset(self):return Comment.objects.filter(user=self.request.user)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def record_view(request,pk):
 video=get_object_or_404(Video,pk=pk)
 Video.objects.filter(pk=pk).update(views=F('views')+1)
 return Response({'views':video.views+1})
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like(request,pk):
 video=get_object_or_404(Video,pk=pk)
 obj,created=Like.objects.get_or_create(user=request.user,video=video)
 if not created:obj.delete()
 return Response({'liked':created,'likes_count':Like.objects.filter(video=video).count()})
class SavedVideos(generics.ListAPIView):
 permission_classes=[permissions.IsAuthenticated];serializer_class=WatchLaterSerializer
 def get_queryset(self):return WatchLater.objects.filter(user=self.request.user).select_related('video','video__category','video__uploaded_by')
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_video(request):
 video=get_object_or_404(Video,pk=request.data.get('video_id'))
 obj,created=WatchLater.objects.get_or_create(user=request.user,video=video)
 return Response({'id':obj.id,'saved':True},status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
class RemoveSaved(generics.DestroyAPIView):
 permission_classes=[permissions.IsAuthenticated]
 def get_queryset(self):return WatchLater.objects.filter(user=self.request.user)
