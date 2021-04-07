"""Project forms."""
from django.forms import ModelForm, Select, Textarea, TextInput

from .models import Post, Subscriber


class PostForm(ModelForm):
    """Post Form."""

    class Meta:
        """Form Meta."""

        model = Post
        fields = ['title', 'description', 'content']
        widgets = {
            "title": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название статьи"
            }),
            "description": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Описание статьи"
            }),
            "content": Textarea(attrs={
                "class": "form-control",
                "placeholder": "Содержимое"
            })
        }


class SubscriberForm(ModelForm):
    """Subscriber Form."""

    class Meta:
        """Subscriber Form Meta."""

        model = Subscriber
        fields = ['email_to', 'author_id']
        widgets = {
            "email_to": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Email подписчика "
            }),
            "author_id": Select(attrs={
                "class": "form-control",
                "placeholder": "Автор ID"
            }),

        }