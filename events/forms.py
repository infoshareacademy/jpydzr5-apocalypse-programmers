from django import forms
from .models import Person, Event, Show, Ticket

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['email', 'password', 'first_name', 'last_name']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_type', 'creator']

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['event', 'start_time', 'end_time', 'price']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['show', 'participant']