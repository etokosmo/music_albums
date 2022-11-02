import re

from rest_framework import generics, filters
from rest_framework.serializers import ModelSerializer, Field, \
    HyperlinkedModelSerializer, ValidationError

from .models import Album, Artist, Track


class AlbumNameField(Field):
    """AlbumField Serializer like 'album[int:year]'"""
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
    """Artist Serializer like Artist.model"""
    class Meta:
        model = Artist
        fields = ['name']

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        super().to_internal_value({'name': data})
        return data


class TrackSerializer(ModelSerializer):
    """Track Serializer like Track.model"""
    class Meta:
        model = Track
        fields = ['name']

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        super().to_internal_value({'name': data})
        return data


class AlbumHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    """Special serializer with field name replacement"""
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
    """Main Album Serializer"""
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
    """Album serializer with ordering, only GET"""
    queryset = Album.objects.all().select_related('artist').prefetch_related(
        'tracks')
    serializer_class = AlbumSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'artist']
