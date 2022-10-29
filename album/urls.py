from django.urls import path

from .views import create_album

app_name = "album"

urlpatterns = [
    path('api/create', create_album),
]
