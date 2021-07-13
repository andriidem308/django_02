"""Filter package."""
import django_filters
from main.models import Book, Post


class PostFilter(django_filters.FilterSet):
    """Class Post Filter."""

    class Meta:
        """Meta class."""

        model = Post
        fields = ['title']


class BooksFilter(django_filters.FilterSet):
    """Class Books Filter."""

    class Meta:
        """Meta class."""

        model = Book
        fields = ['title']
