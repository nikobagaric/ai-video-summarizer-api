from openai import OpenAI

def read_sound(sound_file_path):
    # Read the sound file
    client = OpenAI()

    audio_file = open(sound_file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_formamt="text",
    )

    return transcription.text