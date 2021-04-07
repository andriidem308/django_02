"""Show Posts Method."""
from main.models import Post


def post_all():
    """Post All."""
    objects_all = Post.objects.all()
    return objects_all
