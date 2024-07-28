from django.contrib import admin
from .models import Person, Event, Show, Ticket

admin.site.register(Person)
admin.site.register(Event)
admin.site.register(Show)
admin.site.register(Ticket)