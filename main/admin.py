"""Django admin method."""
from django.contrib import admin
# Register your models here.
from main.models import Author, Comments, Logger, Post, Subscriber


class CommentAdmin(admin.ModelAdmin):
    """Comments Sort."""

    list_display = ("subs_id", "body", "post", "created", "activate")
    list_filter = ("activate", "created", "updated")
    search_fields = ("subs_id", "body")


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Subscriber)
admin.site.register(Logger)
admin.site.register(Comments, CommentAdmin)
