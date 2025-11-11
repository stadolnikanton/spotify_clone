from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.shortcuts import redirect
from app.views import PlaylistView, RegisterView, MainView, ArtistView
from app.views import RateSongView


def google_login(request):
    return redirect('/accounts/google/login/')


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('artist/<int:artist_id>/', ArtistView.as_view(), name='artist'),
    path('songs/<int:song_id>/<str:action>/toggle-favorite/',
         PlaylistView.as_view(), name='toggle_favorite'),
    path('song/<int:song_id>/rate/', RateSongView.as_view(), name='rate_song'),


    path('auth/google/', google_login, name='google_login'),
    path('accounts/', include('allauth.urls')),

]
