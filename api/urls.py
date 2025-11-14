from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .views import SongViewSet, RatingViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='song')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),

    path('auth/login/',
         CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
