"""
Defines Celery tasks that orchestrate the AI functionalities.
"""

from celery import shared_task
from .youtube_utils import download_youtube_video
from .audio_utils import extract_audio_from_video
from .text_processing import transcribe_audio, process_text_with_gpt
from .helpers import cleanup_temp_files
from core import models

@shared_task
def process_youtube_video(url, user_id):
    # Step 1: Download the video
    video_path, temp_dir = download_youtube_video(url)
    
    try:
        # Step 2: Extract the audio
        audio_path = extract_audio_from_video(video_path)
        
        # Step 3: Transcribe the audio
        transcript = transcribe_audio(audio_path)
        
        # Step 4: Process text with GPT
        processed_text = process_text_with_gpt(transcript)
        
        # Step 5: Save the note with a link to the YouTube video
        user = models.User.objects.get(id=user_id)
        note = models.Note.objects.create(user=user, content=processed_text, video_url=url)
        
    finally:
        # Cleanup: Delete temporary files
        cleanup_temp_files(temp_dir)
    
    return note.id
