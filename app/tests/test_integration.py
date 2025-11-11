from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Song, Artist, Genre


class UserFlowTest(TestCase):

    def test_user_registration_and_main_page(self):
        """Полный цикл: регистрация -> главная страница"""
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(User.objects.filter(username='testuser').exists())

        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'songs')

    def test_song_rating_flow(self):
        """Добавление песни и выставление рейтинга"""
        user = User.objects.create_user(
            'testuser', 'test@example.com', 'testpass')
        artist = Artist.objects.create(name='Test Artist')
        genre = Genre.objects.create(name='Test Genre')
        song = Song.objects.create(
            title='Test Song',
            artist=artist,
            genre=genre,
            average_rating=0,
            total_ratings=0
        )

        self.client.force_login(user)

        response = self.client.post(reverse('rate_song', args=[song.id]), {
            'rating': 5
        })

        self.assertEqual(response.status_code, 302)

        self.assertEqual(song.rating_set.count(), 1)
        self.assertEqual(song.rating_set.first().rating, 5)
