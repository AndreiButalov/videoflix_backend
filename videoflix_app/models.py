from django.db import models

class Video(models.Model):
    """Model representing a video in the Videoflix platform.
    
    Stores metadata about videos including title, description, and file references.
    Automatically tracks creation timestamp and supports categorization.
    
    Attributes:
        created_at (DateTimeField): Timestamp of video creation (auto-set).
        title (CharField): Video title (max 255 characters).
        description (TextField): Detailed video description.
        video_file (FileField): Original video file upload (optional).
        thumbnail_url (ImageField): Video thumbnail image (optional).
        category (CharField): Video category/genre classification (max 100 characters).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    thumbnail_url = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    category = models.CharField(max_length=100)

    def __str__(self):
        """Return string representation of the video.
        
        Returns:
            str: The video title.
        """
        return self.title