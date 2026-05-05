from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse, Http404
from rest_framework.permissions import IsAuthenticated
from videoflix_app.models import Video
from .serializers import VideoSerializer
import os
from django.conf import settings

class VideoListView(APIView):
    """Retrieve list of all available videos.
    
    Returns videos sorted by creation date in descending order.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch all videos sorted by newest first.
        
        Args:
            request: HTTP request from authenticated user.
            
        Returns:
            Response: List of serialized video objects with metadata (200).
                     Fields include: id, created_at, title, description, thumbnail_url, category.
        """
        videos = Video.objects.all().order_by("-created_at")

        serializer = VideoSerializer(
            videos,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)
    

class VideoStreamView(APIView):
    """Stream HLS manifest file for video playback.
    
    Returns the HLS playlist (index.m3u8) for the specified video and resolution.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):
        """Retrieve HLS manifest file for video streaming.
        
        Args:
            request: HTTP request from authenticated user.
            movie_id (int): ID of the video to stream.
            resolution (str): Resolution format (e.g., '720p').
            
        Returns:
            FileResponse: HLS manifest file (index.m3u8) with media type application/vnd.apple.mpegurl.
            
        Raises:
            Http404: If video not found or manifest file doesn't exist.
        """
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
    """Stream video segment file for HLS playback.
    
    Returns individual video segments (.ts files) used in HLS streaming.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution, segment):
        """Retrieve a video segment file for streaming.
        
        Args:
            request: HTTP request from authenticated user.
            movie_id (int): ID of the video.
            resolution (str): Resolution format (e.g., '720p').
            segment (str): Segment filename (e.g., 'segment_000.ts').
            
        Returns:
            FileResponse: Video segment file with media type video/MP2T.
            
        Raises:
            Http404: If video not found or segment file doesn't exist.
        """
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