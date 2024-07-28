from django.urls import path
from . import views

urlpatterns = [
    path('people/', views.person_list, name='person_list'),
    path('people/add/', views.person_create, name='person_create'),
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.event_create, name='event_create'),
    # Dodaj URL dla Show i Ticket
]