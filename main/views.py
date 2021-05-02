"""Django Views."""
from time import time

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from faker import Faker
from main.forms import PostForm, SubscriberForm
from main.models import Author, Book, Category, ContactUs, Post, Subscriber
from main.services.notify_service import notify
from main.services.post_service import comment_method, post_all, post_find
from main.services.subscribe_service import subscribe
from main.tasks import notify_subscriber_sync, notify_subscribers


def index(request):
    """Route main page."""
    return render(request, "main/index.html")


def about(request):
    """Route About."""
    return render(request, "main/about.html", {"title": "About Company"})


def posts_all(request):
    """Route Posts."""
    context = {'title': "Posts", "posts": post_all()}
    return render(request, "main/posts_all.html", context)


def post_create(request):
    """Route Create Post."""
    errors = ''
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts_all")
        else:
            errors = "Не возможно сохранить пост."
    else:
        form = PostForm()
    context = {"form": form, "errors": errors}
    return render(request, "main/post_create.html", context=context)


def subscribers_new(request):
    """Route to Subscribe Author."""
    success = False
    email_to = request.POST.get('email_to')
    errors = ''
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
        else:
            errors = form.errors
    else:
        form = SubscriberForm()

    if success:
        notify_subscriber_sync.delay(email_to)
        return redirect('subscribers_all')

    context = {"form": form, "errors": errors}
    return render(request, "main/subscribers_new.html", context=context)


def subscribe_notify(author_id, email_to):
    """Subscribe and Notify."""
    subscribe(author_id, email_to)
    notify(email_to)


def subscribers_all(request):
    """Route to All Subscribers."""
    all_subs = Subscriber.objects.all()
    return render(request, "main/subscribers_all.html", {"title": "Все подписки", "subscribers_all": all_subs})


def email_subscribers(request):
    """Route for Email All Subscribers."""
    start_time = time()
    notify_subscribers.delay()
    end_time = time() - start_time
    print(end_time)
    return redirect('homepage')


def authors_new(request):
    """Generate new Author."""
    fake = Faker()
    Author(name=fake.name(), email=fake.email()).save()
    return redirect("authors_all")


def authors_all(request):
    """Route to Authors List."""
    all_authors = Author.objects.all().prefetch_related('books')
    return render(request, "main/authors_all.html", {"title": "Авторы", "authors": all_authors})


def books(request):
    """Route to Books."""
    all_books = Book.objects.all().select_related('author', 'category')
    return render(request, 'main/books.html', {'title': 'Книги', 'books': all_books})


def categories(request):
    """Route to Categories."""
    all_categories = Category.objects.only('name').distinct().prefetch_related('books')
    return render(request, 'main/categories.html', {'title': 'Категории', 'categories': all_categories})


def post_update(request, post_id):
    """Update Posts."""
    err = ""
    pst = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = PostForm(instance=pst, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts_all")
        else:
            err = "Не возможно обновить пост."
    else:
        form = PostForm(instance=pst)
    context = {
        "form": form,
        "err": err
    }
    return render(request, "main/post_update.html", context=context)


def post_show(request, post_id):
    """Route to Post by ID."""
    pst = post_find(post_id)
    comment_form, comments = comment_method(pst, request)
    return render(request, "main/post_show.html",
                  {"title": pst.title, "pst": pst, "comments": comments, "comment_form": comment_form})


def api_authors_new(request):
    """Route New Author API."""
    fake = Faker()
    Author(name=fake.name(), email=fake.email()).save()
    authors = Author.objects.all().values("name", "email")
    return JsonResponse(list(authors), safe=False)


def api_posts(request):
    """Route Posts API."""
    posts = post_all()
    responded = [dict(title=post.title, description=post.description, content=post.content) for post in posts]
    return JsonResponse(responded, safe=False)


def api_subscribe(request):
    """Route Subscribers API."""
    author_id = request.GET["author_id"]
    email_to = request.GET["email_to "]
    get_object_or_404(Author, pk=author_id)
    subscribe_notify(author_id, email_to)
    data = {"author_id": author_id}
    return JsonResponse(data, safe=False)


class PostsListView(ListView):
    """Show list of posts analogously."""

    queryset = Post.objects.all()
    template_name = "main/post_list.html"


class ContactUsView(CreateView):
    """Create contact us Form as view."""

    success_url = reverse_lazy("homepage")
    model = ContactUs
    fields = ("email", "subject", "msg")
