import debug_toolbar
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from app.views import RegisterView, MainView, ArtisView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('artist/<int:artist_id>/', ArtisView.as_view(), name="artist"),
    path('__debug__/', include(debug_toolbar.urls)),
]
