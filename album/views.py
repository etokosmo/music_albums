import requests
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Field, \
    HyperlinkedModelSerializer, ValidationError
import re
from .models import Album, Artist, Track


class AlbumNameField(Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            pattern = r'.+\[\d+\]'
            result = re.match(pattern, data).group(0)
            if result == data:
                return data
            else:
                raise ValidationError(
                    'Format: album[int:year]'
                )
        except AttributeError:
            raise ValidationError(
                'Format: album[int:year]'
            )


class ArtistSerializer(ModelSerializer):
    class Meta:
        model = Artist
        fields = ['name']

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        super().to_internal_value({'name': data})
        return data


class TrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ['name']

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        super().to_internal_value({'name': data})
        return data


class AlbumHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    field_name_map = {}

    def to_representation(self, instance):
        res = super().to_representation(instance)
        nres = res.__class__()
        for k, v in res.items():
            nres[self.field_name_map.get(k, k)] = v
        return nres

    def to_internal_value(self, data):
        for field in self._writable_fields:
            for name, new_name in self.field_name_map.items():
                if field.field_name == name:
                    field.field_name = new_name
        res = super().to_internal_value(data)
        nres = res.__class__()
        for k, v in res.items():
            nres[self.field_name_map.get(k, k)] = v
        return nres


class AlbumSerializer(AlbumHyperlinkedModelSerializer):
    field_name_map = {
        'artist': 'artist@name'
    }
    album = AlbumNameField()
    artist = ArtistSerializer()
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['album', 'name', 'artist', 'tracks']


class AlbumView(generics.ListAPIView):
    queryset = Album.objects.all().select_related('artist').prefetch_related(
        'tracks')
    serializer_class = AlbumSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'artist']


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
