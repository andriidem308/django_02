"""Django admin method."""
from django.contrib import admin
# Register your models here.
from main.models import Author, Post, Subscriber


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Subscriber)
