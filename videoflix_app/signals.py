from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from videoflix_app.tasks import convert720p


@receiver(post_save.connect, sender=Video)
def create_lecture(sender, instance, created, **kwargs):
    if created:
        print('New object created')
        convert720p(instance.video_file.path)



