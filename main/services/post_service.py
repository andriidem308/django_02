"""Show Posts Method."""
from main.forms import CommentsForm
from main.models import Post


def post_all():
    """Post All."""
    objects_all = Post.objects.all()
    return objects_all


def post_find(post_id: int) -> Post:
    """Post Find."""
    return Post.objects.get(id=post_id)


def comment_method(post, request):
    """Comment Show and Post."""
    comments = post.comments.filter(activate=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentsForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentsForm()
    return comment_form, comments
