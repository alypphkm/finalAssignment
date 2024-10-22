# ABhallbooking/admin.py
from django.contrib import admin
from .models import User, Event, Seat, BookedTicket

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Seat)
admin.site.register(BookedTicket)
