"""Project urls."""
# from django.contrib import admin
# from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from . import views
urlpatterns = [
    # path('', views.index, name='homepage'),
    path('', TemplateView.as_view(template_name='main/index.html'), name='homepage'),
    # url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon/favicon.ico')),
    path('about/', views.about, name='about'),

    path('posts/create/', views.post_create, name='post_create'),
    path('posts/update/<int:post_id>/', views.post_update, name='post_update'),
    path('posts/', views.posts_all, name='posts_all'),
    path('posts/<int:post_id>/', views.post_show, name='post_show'),
    path('posts/list/', views.PostsListView.as_view(), name='post_list'),

    path('subcribers/new/', views.subscribers_new, name='subscribers_new'),
    path('subcribers/all/', views.subscribers_all, name='subscribers_all'),
    path('subscribers/email/', views.email_subscribers, name='email_subscribers'),

    path('authors/new/', views.authors_new, name='authors_new'),
    path('authors/all/', views.authors_all, name='authors_all'),

    path('books/', views.books, name='books'),
    path('categories/', views.categories, name='categories'),

    path('contact-us/create/', views.ContactUsView.as_view(), name='contact-us-create'),

    path('api/posts/', views.api_posts, name='api_posts'),
    path('api/subcribe/', views.api_subscribe, name='api_subscribe'),
    path('api/authors/new/', views.api_authors_new, name='api_authors_new'),
]
