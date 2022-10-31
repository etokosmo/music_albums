from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Field

from .models import Album, Artist, Track


class AlbumNameField(Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return data


class ArtistSerializer(ModelSerializer):
    class Meta:
        model = Artist
        fields = ['name']

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return data


class TrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ['name']

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return data


class AlbumSerializer(ModelSerializer):
    album = AlbumNameField()
    artist = ArtistSerializer()
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['album', 'name', 'artist', 'tracks']


@api_view(['GET', 'POST'])
def handle_album(request):
    if request.method == 'GET':
        albums = Album.objects.all()
        serialize_albums = AlbumSerializer(albums, many=True)
        return Response(serialize_albums.data)
    if request.method == 'POST':
        serializer = AlbumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
