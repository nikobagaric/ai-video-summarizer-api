"""
Handling YouTube videos.
"""
from pytube import YouTube
import os
import tempfile

def download_youtube_video(url):
    yt = YouTube(url)
    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    temp_dir = tempfile.mkdtemp()  # Create a temporary directory
    video_path = os.path.join(temp_dir, 'video.mp4')
    video_stream.download(output_path=temp_dir, filename='video.mp4')
    return video_path, temp_dir  # Return both the video path and the temp directory for cleanup
