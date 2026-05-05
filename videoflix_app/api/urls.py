from django.urls import path
from .views import VideoListView, VideoSegmentView

urlpatterns = [
    path("video/", VideoListView.as_view(), name="video-list"),
    path("video/<int:movie_id>/<str:resolution>/<str:segment>/", VideoSegmentView.as_view(), name="video-segment")  
]