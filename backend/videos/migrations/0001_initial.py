from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Category', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=80, unique=True)), ('slug', models.SlugField(unique=True))]),
        migrations.CreateModel(name='Video', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('title', models.CharField(max_length=200)), ('description', models.TextField(blank=True)), ('video_file', models.FileField(upload_to='videos/')), ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails/')), ('uploaded_at', models.DateTimeField(auto_now_add=True)), ('views', models.PositiveIntegerField(default=0)), ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='videos', to='videos.category')), ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='Comment', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('text', models.TextField(max_length=2000)), ('created_at', models.DateTimeField(auto_now_add=True)), ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='videos.video'))], options={'ordering': ['-created_at']}),
        migrations.CreateModel(name='Like', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='videos.video'))]),
        migrations.CreateModel(name='WatchLater', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('created_at', models.DateTimeField(auto_now_add=True)), ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_videos', to=settings.AUTH_USER_MODEL)), ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video'))], options={'ordering': ['-created_at']}),
        migrations.AddConstraint(model_name='like', constraint=models.UniqueConstraint(fields=('video', 'user'), name='unique_video_like')),
        migrations.AddConstraint(model_name='watchlater', constraint=models.UniqueConstraint(fields=('video', 'user'), name='unique_saved_video')),
    ]
