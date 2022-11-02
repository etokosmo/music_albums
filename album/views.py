import re

import requests
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Album, Artist, Track
from .serializers import AlbumSerializer


def get_year_by_album(album: str) -> int:
    """Return year from AlbumField like 'album[int:year]'"""
    pattern = r'\[(\d+)\]'
    year = re.search(pattern, album).group(1)
    return int(year)


@api_view(['GET', 'POST'])
def handle_album(request) -> Response:
    """API endpoint with serialize album"""
    if request.method == 'GET':
        albums = Album.objects.all().select_related('artist').prefetch_related(
            'tracks')
        serialize_albums = AlbumSerializer(albums, many=True)
        return Response(serialize_albums.data)
    if request.method == 'POST':
        serializer = AlbumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        artist, created = Artist.objects.get_or_create(
            name=serializer.validated_data['artist@name']
        )
        album = Album.objects.create(
            name=serializer.validated_data['name'],
            artist=artist,
            year=get_year_by_album(serializer.validated_data['album'])
        )
        for track in serializer.validated_data['tracks']:
            Track.objects.create(
                name=track,
                album=album
            )
        return Response(serializer.validated_data)


def index(request, sort_key='') -> render:
    """Render main page with albums from db with API"""
    payload = {"ordering": sort_key}
    url = request.build_absolute_uri(reverse_lazy('album:get_album'))
    response = requests.get(url, params=payload)
    response.raise_for_status()
    decoded_response = response.json()
    captions = decoded_response[0].keys()

    context = {'albums': decoded_response, 'captions': captions}
    return render(request, 'album/index.html', context=context)
