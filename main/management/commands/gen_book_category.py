"""Generating Books."""
import random

from django.core.management.base import BaseCommand
from faker import Faker
from main.models import Author, Book, Category


class Command(BaseCommand):
    """Class Command."""

    def handle(self, *args, **kwargs):
        """Procedure which generate books."""
        fake = Faker()

        for _ in range(100):
            Author(name=fake.name(), surname=fake.name(), email=fake.email()).save()

        for cat in open('main/management/commands/categories.txt', 'r'):
            Category(name=cat.rstrip()).save()

        authors = list(Author.objects.all())
        categories = list(Category.objects.all())

        for _ in range(500):
            author, category = random.choice(authors), random.choice(categories)
            Book(title=fake.text(max_nb_chars=25).replace('.', ''), author=author, category=category).save()
