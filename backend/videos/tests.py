from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from .models import Category,Video
class VideoAPITests(TestCase):
 def setUp(self):
  self.user=User.objects.create_user(username='tester',password='SafePassword123!')
  self.cat=Category.objects.create(name='Technology',slug='technology')
  self.client=APIClient()
  self.video=Video.objects.create(title='Django tutorial',category=self.cat,uploaded_by=self.user,video_file=SimpleUploadedFile('test.mp4',b'fake mp4 bytes',content_type='video/mp4'))
 def test_register_login_profile(self):
  r=self.client.post('/api/auth/register/',{'username':'newuser','password':'StrongPassword123!'},format='json');self.assertEqual(r.status_code,201)
  r=self.client.post('/api/auth/login/',{'username':'tester','password':'SafePassword123!'},format='json');self.assertEqual(r.status_code,200)
  self.client.credentials(HTTP_AUTHORIZATION='Bearer '+r.data['access']);self.assertEqual(self.client.get('/api/auth/profile/').status_code,200)
 def test_search_categories_and_view(self):
  self.assertEqual(self.client.get('/api/videos/search/?q=django').data['count'],1)
  self.assertEqual(self.client.get(f'/api/categories/{self.cat.id}/videos/').data['count'],1)
  self.assertEqual(self.client.post(f'/api/videos/{self.video.id}/view/').data['views'],1)
 def test_upload_comment_like_watch_later(self):
  self.client.force_authenticate(self.user)
  upload=self.client.post('/api/videos/upload/',{'title':'New clip','category':self.cat.id,'video_file':SimpleUploadedFile('new.mp4',b'fake video',content_type='video/mp4')},format='multipart');self.assertEqual(upload.status_code,201,upload.data)
  pk=self.video.id
  self.assertEqual(self.client.post(f'/api/videos/{pk}/comments/',{'text':'Nice!'},format='json').status_code,201)
  self.assertEqual(self.client.post(f'/api/videos/{pk}/like/').data['liked'],True)
  self.assertEqual(self.client.post(f'/api/videos/{pk}/like/').data['liked'],False)
  saved=self.client.post('/api/watch-later/add/',{'video_id':pk},format='json');self.assertIn(saved.status_code,[200,201])
  self.assertEqual(self.client.get('/api/watch-later/').data['count'],1)
  self.assertEqual(self.client.delete(f"/api/watch-later/{saved.data['id']}/").status_code,204)
