from django.urls import path

from .serializers import AlbumView
from .views import handle_album, index

app_name = "album"

urlpatterns = [
    path('<str:sort_key>', index, name='index'),
    path('', index, name='index'),
    path('api/', handle_album, name='create_album'),
    path('api/sort/', AlbumView.as_view(), name='get_album'),
]
