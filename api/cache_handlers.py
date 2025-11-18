from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from app.models import Rating

@receiver([post_save, post_delete], sender=Rating)
def clear_song_api_cache(sender, **kwargs):
    cache.clear()

