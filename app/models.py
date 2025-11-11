from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='albums')
    cover = models.ImageField(upload_to='albums/', blank=True, null=True)
    release_year = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} — {self.artist.name}"


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(
        'Artist', on_delete=models.CASCADE, related_name='songs'
    )
    album = models.ForeignKey(
        'Album', on_delete=models.SET_NULL, blank=True, null=True, related_name='songs'
    )
    genre = models.ForeignKey(
        'Genre', on_delete=models.SET_NULL, blank=True, null=True
    )
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)
    average_rating = models.FloatField(default=0)
    total_ratings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} -- {self.artist.name}"

    def update_rating_stats(self):
        stats = self.rating_set.aggregate(
            average=Avg('rating'),
            count=Count('id')
        )

        self.average_rating = round(stats['average'] or 0, 1)
        self.total_ratings = stats['count']
        self.save()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'song']

    def __str__(self):
        return f"{self.rating}"


class Playlist(models.Model):
    title = models.CharField(max_length=200, default="Мой плейлист")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(
        'Song', through='PlaylistSong', related_name='playlists')
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['playlist', 'song']
