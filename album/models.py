from django.db import models


class Artist(models.Model):
    name = models.CharField(
        verbose_name="Имя",
        max_length=200,
    )

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = 'Артисты'

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        verbose_name="Артист",
        related_name='albums',
    )
    year = models.PositiveIntegerField(
        verbose_name='Год'
    )

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'

    def __str__(self):
        return f'{self.name}[{self.year}]'


class Track(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        verbose_name="Альбом",
        related_name='tracks',
    )

    class Meta:
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'

    def __str__(self):
        return self.name
