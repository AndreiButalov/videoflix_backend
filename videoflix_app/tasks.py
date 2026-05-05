import os
import subprocess
from django.conf import settings


def convert_hls(video_id, source):
    """Convert video file to HLS format for streaming.
    
    Transcodes a video file to H.264/AAC format and generates HLS segments
    (index.m3u8 playlist and .ts segment files) for adaptive bitrate streaming.
    
    Args:
        video_id (int): ID of the video being converted.
        source (str): Path to the source video file.
        
    Returns:
        None: Writes HLS files to MEDIA_ROOT/hls/{video_id}/720p/
        
    Note:
        - This is a background job meant to run via RQ queue
        - Requires ffmpeg to be installed on the system
        - Outputs 720p resolution with CRF 23 quality
        - Creates 10-second HLS segments
        - Output directory is created if it doesn't exist
        
    Raises:
        CalledProcessError: If ffmpeg command fails.
    """
    output_dir = os.path.join(
        settings.MEDIA_ROOT,
        "hls",
        str(video_id),
        "720p"
    )

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "index.m3u8")

    cmd = [
        "ffmpeg",
        "-i", source,
        "-vf", "scale=-2:720",
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