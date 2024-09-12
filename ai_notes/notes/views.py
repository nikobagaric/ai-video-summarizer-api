from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from core.models import (
    Notes,
)
from notes import serializers

from utils.youtube_extractor import (download_video, get_video_info, is_valid_youtube_url)
from utils.sound_reader import read_sound
from utils.simple_rag_agent import summarize_text


class NotesViewSet(viewsets.ModelViewSet):
    """Manage notes in the database."""
    serializer_class = serializers.NotesSerializer
    queryset = Notes.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the notes for the authenticated user."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new note."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=False, serializer_class=serializers.YouTubeURLSerializer)
    def process_youtube_url(self, request):
        """Process a YouTube URL to generate a summary and save it as a note."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data['url']

        if not is_valid_youtube_url(url):
            return Response({'error': 'Invalid YouTube URL'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video_path, error = download_video(url)
            if error:
                return Response({'error': f"primary: {error}"}, status=status.HTTP_400_BAD_REQUEST)

            video_info, error = get_video_info(url)
            if error:
                print("VIDEO INFO ERROR")
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

            text = read_sound(video_path)
            if not text:
                print("SOUND READER ERROR")
                return Response({'error': 'Failed to extract audio from the video'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            summary = summarize_text(text)
            if not summary:
                print("SUMM ERROR")
                return Response({'error': 'Failed to generate a summary'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Save the summarized text as a note
            note = Notes.objects.create(
                user=request.user,
                title=video_info.get('title', 'Untitled'),  # Handle missing title
                content=summary
            )

            note_serializer = self.get_serializer(note)
            return Response(note_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'An error occurred while processing the YouTube URL: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
