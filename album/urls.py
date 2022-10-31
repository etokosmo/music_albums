from django.urls import path

from .views import handle_album

app_name = "album"

urlpatterns = [
    path('', handle_album),
]
