from rest_framework import serializers
from videoflix_app.models import Video

class VideoSerializer(serializers.ModelSerializer):
    """Serializer for Video model.
    
    Converts Video instances to JSON and vice versa.
    Represents only essential video information for API responses.
    """
    thumbnail_url = serializers.ImageField(use_url=True)

    class Meta:
        model = Video
        fields = [
            "id",
            "created_at",
            "title",
            "description",
            "thumbnail_url",
            "category",
        ]