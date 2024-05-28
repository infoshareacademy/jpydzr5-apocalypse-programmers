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
            creator_id: int,
    ):
        super().__init__(self)
        self._id = id  # zamienić na generator identyfikatorow, zeby nie bylo duplikatow
        self._name = name  # unikalny indentyfikator wydarzenia
        self.event_type = event_type
        self.start_time = start_time
        self.end_time = end_time
        self.creator_id = creator_id  # relacja do osoby tworzącej wydarzenie


    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    def __str__(self):
        return f"{self._name}"

class Person:
    """Przodek klas związanych z osobami"""
    first_name: str = ''
    last_name: str = ''
    def __init__(
            self,
            id: int,
            email: str,
            password: str
    ):
        self._id = id  # zamienić na generator identyfikatorow, zeby nie bylo duplikatow
        self.email = email  # unikalny indentyfikator osoby
        self.password = password

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Participant(Person):
    """Uczestnik wydarzenia"""
    pass

class EventCreator(Person):
    """Osoba odpowiedzialna za utworzenie wydarzenia"""
    def add_event(
            self,
            id: int,
            name: str,
            event_type: str,
            start_time: datetime,
            end_time: datetime,
    ) -> Event:
        return Event(id, name, event_type, start_time, end_time, self._id)

    def del_event(
            self,
            event: Event,
    ) -> None:
        del Event

    def rename_event(
            self,
            event: Event,
            new_name: str,
    ) -> None:
        Event.name = new_name

    def __str__(self):
        return f"{self.name}"


class Ticket:
    """Pojedynczy bilet"""
    def __init__(
            self,
            id: int,
            event_name: str,
            participant_id: int,
            row: str,
            place: str
    ):
        super().__init__(self)
        self._id = id  # zamienić na generator identyfikatorow, zeby nie bylo duplikatow
        self.event_name = event_name  # relacja do wydarzenia
        self.participant_id = participant_id  # relacja do uczestnika
        self.row = row
        self.place = place
