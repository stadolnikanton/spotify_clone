from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.models import Song, Rating, Artist, Album, Genre


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'title', 'artist']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    album = AlbumSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Song
        fields = [
            'id', 'title', 'artist', 'album', 'genre',
            'audio_file', 'average_rating', 'total_ratings'
        ]


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    song = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'song', 'rating', 'created_at', 'updated_at']


class RateSongSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token
