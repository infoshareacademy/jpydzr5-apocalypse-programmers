"""module with classes"""
from datetime import datetime
from decimal import Decimal


class Event:
    """Przodek klas związanych z wydarzeniem"""
    event_id: int = None

    def __init__(
            self,
            db,
            name: str,
            event_type: str,
            creator_id: int,
            event_id: int = None,
    ):
        self.db = db
        if event_id:
            self.event_id = event_id
            self.db.update_event(event_id, name, event_type)
        else:
            self.event_id = self.db.add_event(name, event_type, creator_id)

        self.event_id, self._name, self.event_type, self.creator_id = self.db.get_event(self.event_id)

    def delete(self):
        self.db.delete_event(self.event_id)

    def update(self):
        self.db.update_event(self.event_id, self._name, self.event_type)

    @classmethod
    def get_by_id(cls, db, event_id):
        row = db.get_event(event_id)
        if row:
            return cls(db, row[1], row[2], row[3], row[0])
        return None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name
        self.update()

    def __str__(self):
        return f"{self._name}"


class Person:
    """Przodek klas związanych z osobami"""
    person_id: int = None
    first_name: str = ''
    last_name: str = ''

    def __init__(
            self,
            db,
            email: str,
            password: str,
            person_id: int = None,
    ):
        self.db = db
        if person_id:
            self.person_id = person_id
            self.db.update_person(person_id, email, password)
        else:
            self.person_id = self.db.add_person(email, password)

        self.person_id, self.email, self.__password = self.db.get_person(self.person_id)

    def delete(self):
        self.db.delete_person(self.person_id)

    def update(self):
        self.db.update_person(self.person_id, self.email, self.__password)

    @classmethod
    def get_by_id(cls, db, person_id):
        row = db.get_person(person_id)
        if row:
            return cls(db, row[1], row[2], row[0])
        return None

    def change_email(self, new_email):
        self.email = new_email
        self.update()

    def change_password(self, new_password):
        self.__password = new_password
        self.update()

    def match_pass(self, test_password: str) -> bool:
        """passwords matching
        """
        if self.__password == test_password:
            return True
        return False

    def __str__(self):
        return f"{self.email}"


class Show:
    def __init__(
            self,
            db,
            event_id: int,
            start_time: datetime,
            end_time: datetime,
            price: Decimal,
            show_id: int = None
    ):
        self.db = db
        if show_id:
            self.show_id = show_id
            self.db.update_show(show_id, start_time, end_time, price)
        else:
            self.show_id = self.db.add_show(event_id, start_time, end_time, price)

        self.show_id, self.event_id, self._start_time, self._end_time, self._price = self.db.get_show(self.show_id)


    def delete(self):
        self.db.delete_show(self.show_id)

    def update(self):
        self.db.update_show(self.show_id, self._start_time, self._end_time, self._price)

    @property
    def start_time(self) -> str:
        return self._start_time

    @start_time.setter
    def start_time(self, new_start_time: datetime):
        self._start_time = new_start_time
        self.update()

    @property
    def end_time(self) -> str:
        return self._end_time

    @end_time.setter
    def end_time(self, new_end_time: datetime):
        self._end_time = new_end_time
        self.update()

    @property
    def price(self) -> str:
        return self._price

    @price.setter
    def price(self, new_price: str):
        self._price = new_price
        self.update()

    @classmethod
    def get_by_id(cls, db, show_id):
        row = db.get_show(show_id)
        if row:
            return cls(db, row[1], row[2], row[3], row[4], row[0])
        return None


class Ticket:
    def __init__(
            self,
            db,
            show_id,
            participant_id,
            ticket_id: int = None
    ):
        self.db = db
        if ticket_id:
            self.ticket_id = ticket_id
            self.db.update_ticket(self.ticket_id, participant_id)
        else:
            self.ticket_id = self.db.add_ticket(show_id, participant_id)

        self.ticket_id, self.show_id, self.participant_id = self.db.get_ticket(self.ticket_id)

    def delete(self):
        self.db.delete_ticket(self.ticket_id)

    def update(self):
        self.db.update_ticket(self.ticket_id, self.participant_id)

    @classmethod
    def get_by_id(cls, db, ticket_id):
        row = db.get_ticket(ticket_id)
        if row:
            return cls(db, row[1], row[2], row[0])
        return None

    def cancel_ticket(self) -> None:
        self.delete()


class Participant(Person):
    def buy_ticket(self, show: Show) -> Ticket:
        return Ticket(self.db, show.show_id, self.person_id)

    def __str__(self) -> str:
        """
        this is class str for present class object.
        :return: public information.
        """
        return f'{self.first_name} {self.last_name} [{self.email}]'


class EventCreator(Person):
    """Osoba odpowiedzialna za utworzenie wydarzenia"""

    def add_event(
            self,
            name: str,
            event_type: str,
    ) -> Event:
        return Event(self.db, name, event_type, self.person_id)

    def del_event(
            self,
            event: Event,
    ) -> None:
        event.delete()

    def rename_event(
            self,
            event: Event,
            new_name: str,
    ) -> None:
        event.name = new_name

    def del_show(
            self,
            show: Show,
    ):
        show.delete()

    def add_show(
            self,
            event: Event,
            start_time: datetime,
            end_time: datetime,
            price: Decimal,
    ) -> Show:
        return Show(self.db, event.event_id, start_time, end_time, price)
