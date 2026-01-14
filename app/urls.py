from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from app.views import register_view, main_view

urlpatterns = [
    path('', main_view, name='main'),
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

try:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
except ImportError:
    pass