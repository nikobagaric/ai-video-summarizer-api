import yt_dlp
import re
import os
import logging

# Download directory
DOWNLOAD_DIR = "/videos"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_video(url):
    try:
        # Ensure the download directory exists
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        ydl_opts = {
            'format': 'bestaudio/best',  # Download best quality audio
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'noplaylist': True,  # Ensure only a single video is downloaded, not the whole playlist
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            return file_path, None
    except Exception as e:
        logger.error(f"Error downloading video from {url}: {e}")
        return None, f"Error: {str(e)}"

def get_video_info(url):
    try:
        ydl_opts = {
            'quiet': True,
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_info = {
                "title": info_dict.get("title"),
                "author": info_dict.get("uploader"),
                "length": info_dict.get("duration"),
                "views": info_dict.get("view_count"),
                "thumbnail": info_dict.get("thumbnail"),
            }
            return video_info, None
    except Exception as e:
        logger.error(f"Error getting video info for {url}: {e}")
        return None, f"Error: {str(e)}"

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+(&\S*)?$"
    return re.match(pattern, url) is not None
