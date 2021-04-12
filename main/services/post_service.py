"""Show Posts Method."""
from main.models import Post


def post_all():
    """Post All."""
    objects_all = Post.objects.all()
    return objects_all


def post_find(post_id: int) -> Post:
    """Post Find."""
    return Post.objects.get(id=post_id)
