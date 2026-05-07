import os
import subprocess

from django.conf import settings
from django.core.files import File

from videoflix_app.models import Video


def convert_hls(video_id, source):
    """
    Convert video file to HLS format for multiple resolutions
    and automatically generate a thumbnail if none exists.
    """

    video = Video.objects.get(id=video_id)
    """    
    Thumbnail automatisch generieren    
    """
    thumbnail_dir = os.path.join(
        settings.MEDIA_ROOT,
        "thumbnails"
    )

    os.makedirs(thumbnail_dir, exist_ok=True)

    thumbnail_path = os.path.join(
        thumbnail_dir,
        f"video_{video_id}.jpg"
    )

    if not video.thumbnail_url:

        thumbnail_cmd = [
            "ffmpeg",
            "-i", source,
            "-ss", "00:00:05",
            "-vframes", "1",
            thumbnail_path
        ]

        subprocess.run(thumbnail_cmd, check=True)

        with open(thumbnail_path, "rb") as f:
            video.thumbnail_url.save(
                f"video_{video_id}.jpg",
                File(f),
                save=True
            )

    resolutions = [
        {"name": "480p", "scale": "scale=-2:480"},
        {"name": "720p", "scale": "scale=-2:720"},
        {"name": "1080p", "scale": "scale=-2:1080"},
    ]

    for resolution in resolutions:

        output_dir = os.path.join(
            settings.MEDIA_ROOT,
            "hls",
            str(video_id),
            resolution["name"]
        )

        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(
            output_dir,
            "index.m3u8"
        )

        cmd = [
            "ffmpeg",
            "-i", source,
            "-vf", resolution["scale"],
            "-c:v", "libx264",
            "-c:a", "aac",
            "-crf", "23",
            "-preset", "fast",
            "-hls_time", "10",
            "-hls_playlist_type", "vod",
            "-hls_segment_filename",
            os.path.join(output_dir, "segment_%03d.ts"),
            output_file
        ]

        subprocess.run(cmd, check=True)