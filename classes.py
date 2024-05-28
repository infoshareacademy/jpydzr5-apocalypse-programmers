"""module with classes"""
from datetime import datetime


class Event:
    """Przodek klas związanych z wydarzeniem"""
    def __init__(
            self,
            id: int,
            name: str,
            event_type: str,
            start_time:datetime,
            end_time: datetime,
            creator_email: str
    ):
        super().__init__(self)
        self.id = id  # zamienić na generator identyfikatorow, zeby nie bylo duplikatow
        self.name = name  # unikalny indentyfikator wydarzenia
        self.event_type = event_type
        self.start_time = start_time
        self.end_time = end_time
        self.creator_email = creator_email  # relacja do osoby tworzącej wydarzenie


class Person:
    """Przodek klas związanych z osobami"""
    def __init__(
            self,
            id: int,
            email: str,
            password: str
    ):
        self.id = id  # zamienić na generator identyfikatorow, zeby nie bylo duplikatow
        self.email = email  # unikalny indentyfikator osoby
        self.password = password

class Participant(Person):
    """Uczestnik wydarzenia"""
    pass

class EventCreator(Person):
    """Osoba odpowiedzialna za utworzenie wydarzenia"""
    pass


class Ticket:
    """Pojedynczy bilet"""
    def __init__(
            self,
            id: int,
            event_name: str,
            participant_email: str,
            row: str,
            place: str
    ):
        super().__init__(self)
        self.id = id  # zamienić na generator identyfikatorow, zeby nie bylo duplikatow
        self.event_name = event_name  # relacja do wydarzenia
        self.participant_email = participant_email  # relacja do uczestnika
        self.row = row
        self.place = place
