from pytubefix import YouTube
import re
import os
import logging

# Download directory
DOWNLOAD_DIR = "/videos"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_video(url): # WORKS!!!!!!!!
    try:
        yt = YouTube(url)
        print(yt.title)
        stream = yt.streams.get_audio_only()
        print("something?")

        # Check if a valid audio stream was found
        if stream:
            # Ensure the download directory exists
            print(stream)
            if not os.path.exists(DOWNLOAD_DIR):
                os.makedirs(DOWNLOAD_DIR)

            # Download the video
            return stream.download(output_path=DOWNLOAD_DIR, mp3=True), None
        else:
            logger.error(f"No audio stream found for URL: {url}")
            return None, "Audio stream not found"
    except Exception as e:
        logger.error(f"Error downloading video from {url}: {e}")
        return None, f"Error: {str(e)}"

def get_video_info(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.first()

        # Check if streams are available
        if stream:
            video_info = {
                "title": yt.title,
                "author": yt.author,
                "length": yt.length,
                "views": yt.views,
                "thumbnail": yt.thumbnail_url,
            }
            return video_info, None
        else:
            logger.error(f"No streams found for URL: {url}")
            return None, "Video stream not found"
    except Exception as e:
        logger.error(f"Error getting video info for {url}: {e}")
        return None, f"Error: {str(e)}"

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+(&\S*)?$"
    return re.match(pattern, url) is not None