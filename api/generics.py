"""API Mode Serializers."""
from main.models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """PostSerializer class."""

    class Meta:
        """PostSerializer Meta class."""

        model = Post
        fields = (
            'id',
            'title',
            'description',
            'content',
            'mood',
            'updated',
            'created',
            'get_mood_display'
        )
