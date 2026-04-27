from rest_framework import serializers
from models import Video

class VideoSerializer(serializers.ModelSerializer):
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