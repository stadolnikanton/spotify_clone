from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 

from api.views import SongViewSet, RatingViewSet, SongListAPIView
from api.views import RegisterAPIView, LogoutAPIView


router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='song')
router.register(r'ratings', RatingViewSet, basename='rating')


urlpatterns = [
    path('', include(router.urls)),
    path('songs/', SongListAPIView.as_view(), name='all_songs'),

    #login
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_paar'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
]
