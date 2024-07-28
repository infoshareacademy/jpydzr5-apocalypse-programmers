from django.db import models
from decimal import Decimal
from datetime import datetime

class Person(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.email

class Event(models.Model):
    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Show(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Ticket(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    participant = models.ForeignKey(Person, on_delete=models.CASCADE)