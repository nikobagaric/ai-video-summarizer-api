"""
Handling extracting audio from videos
"""
import subprocess
import os

def extract_audio_from_video(video_path):
    audio_path = os.path.join(os.path.dirname(video_path), 'audio.wav')
    command = f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path} -y"
    subprocess.run(command, shell=True, check=True)
    return audio_path
