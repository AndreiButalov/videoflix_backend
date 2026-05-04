from django.db.models.signals import post_save
from django.dispatch import receiver
import django_rq
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from videoflix_app.tasks import convert_hls


@receiver(post_save, sender=Video)
def create_lecture(sender, instance, created, **kwargs):
    if created and instance.video_file:
        try:
            file_path = instance.video_file.path
        except NotImplementedError:
            print("No local file path available")
            return

        print(f"New video uploaded: {file_path}")

        queue = django_rq.get_queue('default')
        queue.enqueue(convert_hls, instance.id, file_path)



