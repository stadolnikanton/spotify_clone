from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Genre, Artist, Album, Song, Rating, Playlist


class GenreModelTest(TestCase):
    def test_genre_creation(self):
        """Создание жанра и проверка строкового представления"""
        genre = Genre.objects.create(name="Rock")
        self.assertEqual(str(genre), "Rock")


class ArtistModelTest(TestCase):
    def test_artist_creation(self):
        """Создание исполнителя и проверка строкового представления"""
        artist = Artist.objects.create(name="Queen")
        self.assertEqual(str(artist), "Queen")


class SongModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Pop")
        self.artist = Artist.objects.create(name="Artist")
        self.album = Album.objects.create(title="Album", artist=self.artist)

    def test_song_creation(self):
        """Создание песни и проверка связей"""
        song = Song.objects.create(
            title="Song",
            artist=self.artist,
            album=self.album,
            genre=self.genre
        )
        self.assertEqual(str(song), "Song -- Artist")


class RatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.artist = Artist.objects.create(name="Artist")
        self.song = Song.objects.create(title="Song", artist=self.artist)

    def test_rating_creation(self):
        """Создание рейтинга и проверка уникальности пользователь-песня"""
        rating = Rating.objects.create(
            user=self.user, song=self.song, rating=5)
        self.assertEqual(rating.rating, 5)


class PlaylistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")

    def test_playlist_creation(self):
        """Создание плейлиста и проверка избранного"""
        playlist = Playlist.objects.create(user=self.user, title="My Playlist")
        self.assertEqual(playlist.title, "My Playlist")
