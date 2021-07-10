"""Project urls."""
# from django.contrib import admin
# from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators import cache
from django.views.generic import TemplateView

from django_02 import settings
from . import views

urlpatterns = [
    # path('', views.index, name='homepage'),
    path('', TemplateView.as_view(template_name='main/index.html'), name='homepage'),
    # url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon/favicon.ico')),
    path('about/', views.about, name='about'),

    path('posts/create/', views.post_create, name='post_create'),
    path('posts/update/<int:post_id>/', views.post_update, name='post_update'),
    path('posts/<int:pk>/delete/', views.DeletePostView.as_view(), name='post_delete'),
    path('posts/', views.posts_all, name='posts_all'),
    path('posts/<int:post_id>/', views.post_show, name='post_show'),
    # path('posts/list/', views.PostsListView.as_view(), name='post_list'),
    path('posts/list/', cache.cache_page(120)(views.PostsListView.as_view()), name='post_list'),

    path('subcribers/new/', views.subscribers_new, name='subscribers_new'),
    path('subcribers/all/', views.subscribers_all, name='subscribers_all'),
    path('subscribers/email/', views.email_subscribers, name='email_subscribers'),

    path('authors/new/', views.authors_new, name='authors_new'),
    # path('authors/all/', views.authors_all, name='authors_all'),
    # path('authors/all/', cache.cache_page(120)(views.authors_all), name='authors_all'),
    path('authors/<int:pk>/delete/', views.DeleteAuthorsView.as_view(), name='author_delete'),
    path('authors/all/', views.AuthorsListView.as_view(), name='authors_all'),

    path('books/', views.books, name='books'),
    # path('categories/', views.categories, name='categories'),
    path('categories/', cache.cache_page(120)(views.categories), name='categories'),

    path('contact-us/create/', views.ContactUsView.as_view(), name='contact-us-create'),

    path('posts/list/xlsx', views.DownloadPostsXLSX.as_view(), name='posts_xlsx'),

    path('api/posts/', views.api_posts, name='api_posts'),
    path('api/subcribe/', views.api_subscribe, name='api_subscribe'),
    path('api/authors/new/', views.api_authors_new, name='api_authors_new'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
