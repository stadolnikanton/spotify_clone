from debug_toolbar.store import serialize
from rest_framework import viewsets, status
from rest_framework.authentication import authenticate
from rest_framework.decorators import action, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


from app.models import Song, Rating
from api.serializers import SongSerializer, RatingSerializer, RateSongSerializer
from api.serializers import RegisterSerializer


class SongListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)

        return Response(serializer.data)


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
    permission_vclasses = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'username': user.username
            })

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        refresh_token = request.data.get('refresh_token', '')
        
        if not refresh_token:
            return Response({"error": "Нужен refresh_token"})
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'success': "Выход успешен"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Неверный Refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        
