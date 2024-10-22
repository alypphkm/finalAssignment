# ABhallbooking/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, Seat

@receiver(post_save, sender=Event)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for i in range(1, 101):
            Seat.objects.create(event=instance, seat_number=i)
