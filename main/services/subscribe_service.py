"""Subscribe."""
from django.core.exceptions import ObjectDoesNotExist
from main.models import Author
from main.models import Subscriber


def subscribe(author_id, email_to):
    """Subscribe Method."""
    try:
        # TODO get email of Subscriber
        Subscriber.objects.get(email_to=email_to, author_id=int(author_id))
        return False
    except ObjectDoesNotExist:
        author = Author.objects.get(id=author_id)
        subscriber = Subscriber(email_to=email_to, author_id=author)
        # TODO Subscriber.save()
        subscriber.save()
        return True
