from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal


rating_changed = Signal()


def register_rating_signals():
    from app.models import Rating
    
    @receiver(post_save, sender=Rating)
    def on_rating_save(sender, instance, created, **kwargs):
        rating_changed.send(sender=Rating, instance=instance, created=created)
    
    @receiver(post_delete, sender=Rating)
    def on_rating_delete(sender, instance, **kwargs):
        rating_changed.send(sender=Rating, instance=instance, deleted=True)
