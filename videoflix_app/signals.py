from django.db.models.signals import post_save
from django.dispatch import receiver
import django_rq
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from videoflix_app.tasks import convert_hls


@receiver(post_save, sender=Video)
def create_lecture(sender, instance, created, **kwargs):
    """Signal handler to process newly uploaded videos.
    
    Automatically enqueues video conversion to HLS format when a new video
    is uploaded to the system. Queues the job in the RQ background worker.
    
    Args:
        sender: The Video model class (auto-passed by Django signals).
        instance (Video): The Video instance that was created/saved.
        created (bool): True if the instance was just created (not updated).
        **kwargs: Additional signal arguments.
        
    Note:
        - Only processes newly created videos (created=True)
        - Skips processing if video_file is not provided
        - Handles NotImplementedError for cloud storage backends gracefully
        - Job is enqueued in 'default' RQ queue for async processing
    """
    if created and instance.video_file:
        try:
            file_path = instance.video_file.path
        except NotImplementedError:
            print("No local file path available")
            return

        print(f"New video uploaded: {file_path}")

        queue = django_rq.get_queue('default')
        queue.enqueue(convert_hls, instance.id, file_path)



