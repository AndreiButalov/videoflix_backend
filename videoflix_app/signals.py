from django.db.models.signals import post_save
from .models import Video

def create_lecture(sender, instance, created, **kwargs):
    if created:
        print('New object created')



post_save.connect(create_lecture, sender=Video)