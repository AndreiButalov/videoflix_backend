from django.db import models

class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    thumbnail_url = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title