"""API Mode Serializers."""
from main.models import Book, Post
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


class BooksSerializer(serializers.ModelSerializer):
    """Serializer class."""

    class Meta:
        """Meta class."""

        model = Book
        fields = (
            'id',
            'title',
            'author',
            'category',
        )
