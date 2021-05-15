"""Project Models."""
from datetime import datetime

from django.core.cache import cache
from django.db import models
from django.utils.timezone import now

# Create your models here.


class Author(models.Model):
    """Author Model."""

    class Meta:
        """Author Model Meta."""

        db_table = "tb_users"
        verbose_name_plural = "Авторы"
        verbose_name = "Автор"
    name = models.CharField("Имя автора", max_length=90)
    surname = models.CharField("Фамилия автора", max_length=90, blank=True)
    email = models.EmailField("Почта автора", max_length=80)
    """Setup name and email fields types and lengths."""

    def __str__(self):
        """Print Author name."""
        return self.name

    def get_full_name(self):
        """Get Author Full Name."""
        return f'{self.name} {self.surname}'

    @property
    def full_name(self):
        """Print Author Full Name."""
        return f'{self.name} {self.surname}'

    def save(self, **kwargs):
        """Save in custom method for cache_page."""
        super().save()
        key = self.__class__.cache_key()
        cache.delete(key)

    def delete(self, **kwargs):
        """Delete in custom method for cache_page."""
        super().delete()
        key = self.__class__.cache_key()
        cache.delete(key)

    @classmethod
    def cache_key(cls):
        """Save in custom cached method."""
        dt = datetime.today().strftime('%y-%m-%d')
        key = f'{dt}'
        return key


class Book(models.Model):
    """Book Model."""

    class Meta:
        """Book Meta."""

        db_table = 'tb_books'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    title = models.CharField('Заголовок', max_length=40)
    author = models.ForeignKey('Author', models.CASCADE, related_name='books')
    category = models.ForeignKey('Category', models.CASCADE, related_name='books')

    def __str__(self):
        """Print Book."""
        return self.title


class Category(models.Model):
    """Category Model."""

    class Meta:
        """Category Meta."""

        db_table = 'tb_categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField('Категория', max_length=40)

    def __str__(self):
        """Print Category."""
        return self.name


class Subscriber(models.Model):
    """Subscriber Model."""

    class Meta:
        """Subscriber Model Meta."""

        unique_together = ['email_to', 'author_id']
        db_table = "tb_subscribers"
        verbose_name_plural = "Подписчики"
        verbose_name = "Подписчик"

    email_to = models.EmailField("Почта подписчика", max_length=80)
    author_id = models.ForeignKey("Author", on_delete=models.CASCADE)

    def __str__(self):
        """Print Author Email."""
        return self.email_to


class Post(models.Model):
    """Post Model."""

    class Meta:
        """Post Model Meta."""

        db_table = "tb_posts"
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
    """Setup title, description, content and dates of posts."""
    title = models.CharField("Заголовок поста", max_length=70)
    description = models.TextField("Описание поста", max_length=90)
    content = models.TextField("Контент поста")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=now)

    def __str__(self):
        """Print Post Title."""
        return self.title

    def save(self, **kwargs):
        """Save Post."""
        super().save()
        key = self.__class__.cache_key()
        cache.delete(key)

    @classmethod
    def cache_key(cls):
        """Get Cache Key."""
        dt = datetime.today().strftime('%Y-%m-%d')
        key = f'{dt}'
        return key


class Logger(models.Model):
    """Class Logger."""

    class Meta:
        """Logger Meta."""

        db_table = "tb_loggers"

    utm = models.CharField("UTM метка", max_length=50)
    time_execution = models.CharField("Время выполнения", max_length=70)
    created = models.DateTimeField(auto_now_add=True)
    path = models.CharField("Path", max_length=70)
    user_ip = models.CharField("IP адрес пользователя", max_length=20)

    def __str__(self):
        """Print Logger UTM."""
        return self.utm


class Comments(models.Model):
    """Comments Class."""

    class Meta:
        """Comments Meta."""

        db_table = "tb_comments"
        ordering = ("created",)

    post = models.ForeignKey("Post", related_name="comments", on_delete=models.CASCADE)
    body = models.TextField("Комментариий")
    subs_id = models.ForeignKey("Subscriber", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=now)
    activate = models.BooleanField(default=True)

    def __str__(self):
        """Print Comment."""
        return "Comment by {} on {}".format(self.subs_id, self.post)


class ContactUs(models.Model):
    """Contact Us Model."""

    email = models.EmailField()
    subject = models.CharField(max_length=120)
    msg = models.TextField()
