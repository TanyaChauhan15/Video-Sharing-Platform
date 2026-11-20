from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.conf import settings
from videos.models import Category,Video,Comment,Like,WatchLater
from pathlib import Path
class Command(BaseCommand):
 help='Seed categories, demo users and locally generated demo videos (requires ffmpeg for playable clips).'
 def handle(self,*args,**kwargs):
  cats={}
  for name in ['Technology','Gaming','Education','Music','Sports','Entertainment']:
   c,_=Category.objects.get_or_create(slug=name.lower(),defaults={'name':name});cats[name]=c
  users=[]
  for username in ['demo','creator']:
   user,created=User.objects.get_or_create(username=username,defaults={'email':username+'@example.com'})
   if created:user.set_password('DemoPass123!');user.save()
   users.append(user)
  import shutil,subprocess,tempfile
  ffmpeg=shutil.which('ffmpeg')
  if not ffmpeg:self.stdout.write(self.style.WARNING('ffmpeg not installed: categories/users created; upload your own MP4/WebM to populate videos.'));return
  for i,(name,category) in enumerate([(f'{cat} • Studio showcase',cat) for cat in cats],1):
   if Video.objects.filter(title=name).exists():continue
   with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'clip.mp4'
    color=['0x1e293b','0x312e81','0x164e63','0x3f3f46','0x064e3b','0x4c1d95'][i-1]
    subprocess.run([ffmpeg,'-loglevel','error','-y','-f','lavfi','-i',f'color=c={color}:s=640x360:r=24','-f','lavfi','-i','anullsrc=r=44100:cl=stereo','-t','4','-c:v','mpeg4','-q:v','5','-c:a','aac','-shortest',str(path)],check=True)
    video=Video(title=name,description=f'A short locally generated sample for {category}. Upload your own content to explore the platform.',category=cats[category],uploaded_by=users[i%2]);video.video_file.save(f'demo_{i}.mp4',ContentFile(path.read_bytes()),save=True)
    Comment.objects.create(video=video,user=users[0],text='Great demo clip!')
    Like.objects.get_or_create(video=video,user=users[0])
    if i==1:WatchLater.objects.get_or_create(video=video,user=users[0])
  self.stdout.write(self.style.SUCCESS('Demo content ready. demo / DemoPass123!'))
