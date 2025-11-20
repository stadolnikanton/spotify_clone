from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.models import Song, Rating, Artist, Album, Genre, User


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


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangeRateSongSerializer(serializers.ModelSerializer):
    new_rating = serializers.IntegerField(
        min_value=0,
        max_value=5,
        required=True,
        help_text="For test"
    )

    class Meta:
        model = Rating
        fields = ('rating')

    def update(self, instance, validated_data):
        instance = validated_data
        instance.save()
