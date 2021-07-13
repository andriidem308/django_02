"""API urls."""

from api.views import BooksAPIViewSet, PostAPIViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(prefix='posts', viewset=PostAPIViewSet, basename='post')
router.register(prefix='books_view', viewset=BooksAPIViewSet, basename='book')

urlpatterns = router.urls
