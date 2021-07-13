"""API urls."""

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix='posts', viewset=views.PostAPIViewSet, basename='post')

urlpatterns = router.urls
