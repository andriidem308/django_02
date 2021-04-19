"""Project forms."""
from django import forms
from django.forms import ModelForm, Select, Textarea, TextInput

from .models import Author, Comments, Post, Subscriber


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

        def save(self, commit=True):
            """Manual save method for Subscriber."""
            print("Subscriber before save")
            # form.ModelForm.save(self,commit)
            sbr = super().save(commit=False)
            sbr.email_to = sbr.email_to.title()
            sbr.save()
            return sbr


class CommentsForm(ModelForm):
    """CommentsForm Class."""

    class Meta:
        """CommentsForm Meta."""

        model = Comments
        fields = ['body', 'subs_id']
        widgets = {
            "body": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ваш комментариий"
            }

            ),
            "subs_id": Select(attrs={
                "class": "form-control",
                "placeholder": "подписчика ID"
            }),

        }


class SubscriberForm(ModelForm):
    """Subscriber Form."""

    author_id = forms.ModelChoiceField(
        queryset=Author.objects.all().order_by('name'),
        empty_label="Выберите автора",
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        """Subscriber Form Meta."""

        model = Subscriber
        fields = ['email_to', 'author_id']
        widgets = {
            "email_to": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Email подписчика "
            }
            ),
        }
