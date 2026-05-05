import os
import subprocess
from django.conf import settings


def convert_hls(video_id, source):
    """Convert video file to HLS format for multiple resolutions.
    
    Transcodes a video file to H.264/AAC format and generates HLS segments
    for 480p, 720p, and 1080p resolutions.
    (index.m3u8 playlist and .ts segment files) for adaptive bitrate streaming.
    
    Args:
        video_id (int): ID of the video being converted.
        source (str): Path to the source video file.
        
    Returns:
        None: Writes HLS files to MEDIA_ROOT/hls/{video_id}/{resolution}/
        
    Note:
        - This is a background job meant to run via RQ queue
        - Requires ffmpeg to be installed on the system
        - Generates 480p, 720p, and 1080p versions
        - Creates 10-second HLS segments for each resolution
        - Output directories are created if they don't exist
        - Quality (CRF 23) is consistent across all resolutions
        
    Raises:
        CalledProcessError: If ffmpeg command fails.
    """
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

        output_file = os.path.join(output_dir, "index.m3u8")

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
            "-hls_segment_filename", os.path.join(output_dir, "segment_%03d.ts"),
            output_file
        ]

        subprocess.run(cmd)