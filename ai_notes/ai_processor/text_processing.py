"""
Handling text operations with AI
"""

from openai import OpenAI
import io

def transcribe_audio(audio_path): # TODO -> handle 10+ minute vids
    """
    Audio file transcription using Whisper AI
    """
    client = OpenAI()
    audio_file = open(audio_path)
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcription

def process_text_with_gpt(text): # TODO -> handle long text
    client = OpenAI() # TODO -> maybe not use ChatGPT

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are going to summarize the given text in the style of notes taking."},
            {"role": "user", "content": text},
        ]
    )

    return response