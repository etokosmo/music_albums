import requests
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Album
from .serializers import AlbumSerializer


@api_view(['GET', 'POST'])
def handle_album(request):
    if request.method == 'GET':
        albums = Album.objects.all().select_related('artist').prefetch_related(
            'tracks')
        serialize_albums = AlbumSerializer(albums, many=True)
        return Response(serialize_albums.data)
    if request.method == 'POST':
        serializer = AlbumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


def index(request, sort_key=''):
    payload = {"ordering": sort_key}
    url = request.build_absolute_uri(reverse_lazy('album:get_album'))
    response = requests.get(url, params=payload)
    response.raise_for_status()
    decoded_response = response.json()
    captions = decoded_response[0].keys()

    context = {'albums': decoded_response, 'captions': captions}
    return render(request, 'album/index.html', context=context)
