from rest_framework import serializers

from core.models import (
    Notes,
)

class NotesSerializer(serializers.ModelSerializer):
    """Serializer for notes."""

    class Meta:
        model = Notes
        fields = ['id', 'title', 'content']
        read_only_fields = ['id']


class YouTubeURLSerializer(serializers.Serializer):
    url = serializers.URLField()