"""Fill Posts."""

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from main.models import Post
import requests


class Command(BaseCommand):
    """Command class."""

    url = 'https://doroshenkoaa.ru/med/'

    def handle(self, *args, **options):
        """Command handle."""
        Post.objects.all().delete()
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")
        links = []

        for lst in soup.findAll("a", {"class": "more"}):
            links.append(lst.get('href'))

        for lst in links:
            r = requests.get(lst)
            soup = BeautifulSoup(r.text, "html.parser")

            for con in soup.findAll("div", {"itemprop": "articleBody"}):
                content = con.text
            for tit in soup.findAll("h1", {"itemprop": "headline"}):
                title = tit.text.strip()

            Post.objects.create(title=title, content=content)
