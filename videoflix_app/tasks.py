import os
import subprocess
from django.conf import settings


def convert_hls(video_id, source):
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