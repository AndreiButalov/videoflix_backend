from django.db import models

class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.ImageField(upload_to='thumbnails/')
    category = models.CharField(max_length=100)

    # # optional: Pfad zum HLS-Ordner (z.B. /media/hls/movie_1/)
    # hls_path = models.CharField(max_length=500)

    def __str__(self):
        return self.title