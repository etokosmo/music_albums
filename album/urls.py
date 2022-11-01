from django.urls import path

from .views import handle_album, index, AlbumView

app_name = "album"

urlpatterns = [
    path('<str:sort_key>', index, name='index'),
    path('', index, name='index'),
    path('api/', handle_album, name='create_album'),
    path('api/sort/', AlbumView.as_view(), name='get_album'),
]
