from book_tracker.views import BookViewSet
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register("books", BookViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "book_tracker"
