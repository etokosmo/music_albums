from django.urls import path, include

from .views import handle_album, AlbumView

app_name = "album"

urlpatterns = [
    path('api/', handle_album, name='album'),
    path('api/sort/', AlbumView.as_view()),
]
