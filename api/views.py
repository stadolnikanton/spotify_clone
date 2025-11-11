from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from app.models import Song, Rating
from api.serializers import SongSerializer, RatingSerializer, RateSongSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post', 'put'])
    def rate(self, request, pk=None):
        song = self.get_object()
        serializer = RateSongSerializer(data=request.data)

        if serializer.is_valid():
            rating_value = serializer.validated_data['rating']

            rating, created = Rating.objects.update_or_create(
                user=request.user,
                song=song,
                defaults={'rating': rating_value}
            )

            song.update_rating_stats()

            return Response({
                'status': 'rating set',
                'rating': rating_value,
                'average_rating': song.average_rating,
                'total_ratings': song.total_ratings
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def my_rating(self, request, pk=None):
        song = self.get_object()
        try:
            rating = Rating.objects.get(user=request.user, song=song)
            return Response({'my_rating': rating.rating})
        except Rating.DoesNotExist:
            return Response({'my_rating': None})


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
