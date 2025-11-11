from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


from app.forms import RegisterForm
from app.models import Genre, Playlist, Song, Artist, Rating


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)

            return redirect('main')


class MainView(View):
    def get(self, request):
        genres = Genre.objects.all()
        genre_id = request.GET.get('genre')
        query = request.GET.get('q')
        songs = Song.objects.all()

        user_favorite_songs = []
        user_ratings_dict = {}

        if request.user.is_authenticated:
            favorite_playlist = Playlist.objects.filter(
                user=request.user,
                is_favorite=True
            ).first()
            if favorite_playlist:
                user_favorite_songs = favorite_playlist.songs.all()

            user_ratings = Rating.objects.filter(
                user=request.user,
                song__in=songs
            ).select_related('song')

            user_ratings_dict = {
                rating.song_id: rating.rating for rating in user_ratings}

        if genre_id:
            songs = songs.filter(genre_id=genre_id)
        if query:
            songs = songs.filter(
                Q(title__icontains=query) |
                Q(artist__name__icontains=query)
            )

        for song in songs:
            song.user_rating = user_ratings_dict.get(song.id)
            song.is_favorite = song in user_favorite_songs

        return render(request, 'main.html', {
            'songs': songs,
            'genres': genres,
            'selected_genre': genre_id,
            'user_favorite_songs': user_favorite_songs,
        })


class ArtistView(View):
    def get(self, request, artist_id):
        artist = Artist.objects.get(id=artist_id)
        return render(request, "profile_artist.html", {"artist": artist})


class PlaylistView(View):
    def post(self, request, song_id, action):
        song = get_object_or_404(Song, id=song_id)
        if action == "toggle":
            favorite_playlist, created = Playlist.objects.get_or_create(
                user=request.user,
                is_favorite=True,
                defaults={'title': 'Мои любимые треки'}
            )

            if favorite_playlist.songs.filter(id=song_id).exists():
                favorite_playlist.songs.remove(song)
                messages.success(request, f'Песня "{
                    song.title}" удалена из избранного')
            else:
                favorite_playlist.songs.add(song)
                messages.success(request, f'Песня "{
                    song.title}" добавлена в избранное')

            return redirect('/')

        elif action == "delete":
            print("delete")
            favorite_playlist, created = Playlist.objects.get_or_create(
                user=request.user,
                is_favorite=True,
                defaults={'title': 'Мои любимые треки'}
            )

            if favorite_playlist.songs.filter(id=song_id).exists():
                favorite_playlist.songs.remove(song)
                messages.success(request, f'Песня "{
                    song.title}" удалена из избранного')

            return redirect('/')


class RateSongView(LoginRequiredMixin, View):

    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        rating_value = int(request.POST.get('rating', 0))

        if 1 <= rating_value <= 5:
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                song=song,
                defaults={'rating': rating_value}
            )

            song.update_rating_stats()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'rating': rating_value,
                    'average_rating': float(song.average_rating),
                    'total_ratings': song.total_ratings,
                    'is_new': created
                })

        return redirect(request.META.get('HTTP_REFERER', 'main'))
