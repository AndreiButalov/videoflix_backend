from django.db.models.signals import post_save

def create_lecture(sender, instance, created, **kwargs):
    if created:
        print('New object created')