from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse, Http404
from rest_framework.permissions import IsAuthenticated
from videoflix_app.models import Video
from .serializers import VideoSerializer
from rest_framework.permissions import IsAuthenticated
import os
from django.conf import settings

class VideoListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.all().order_by("-created_at")

        serializer = VideoSerializer(
            videos,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)
    

class VideoStreamView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):
        try:
            Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

        path = os.path.join(
            settings.MEDIA_ROOT,
            "hls",
            str(movie_id),
            resolution,
            "index.m3u8"
        )

        if not os.path.exists(path):
            raise Http404("Manifest not found")

        return FileResponse(
            open(path, "rb"),
            content_type="application/vnd.apple.mpegurl"
        )
    

class VideoSegmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution, segment):
        try:
            Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

        path = os.path.join(
            settings.MEDIA_ROOT,
            "hls",
            str(movie_id),
            resolution,
            segment
        )

        if not os.path.exists(path):
            raise Http404("Segment not found")

        return FileResponse(
            open(path, "rb"),
            content_type="video/MP2T"
        )