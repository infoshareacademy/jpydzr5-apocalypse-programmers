"""module with classes"""
from datetime import datetime
from decimal import Decimal


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

        self.person_id, self.email, self.__password = self.db.get_person_by_id(self.person_id)

    def delete(self):
        self.db.delete_person(self.person_id)

    def update(self):
        self.db.update_person(self.person_id, self.email, self.__password)

    @classmethod
    def get_by_id(cls, db, person_id):
        row = db.get_person_by_id(person_id)
        if row:
            return cls(db, row[1], row[2], row[0])
        return None

    def change_email(self, new_email):
        self.email = new_email
        self.update()

    def change_password(self, new_password):
        self.__password = new_password
        self.update()

    @classmethod
    def login_person(cls, db, email, test_password: str):
        row = db.login_person(email, test_password)
        if row:
            return cls(db, row[1], row[2], row[0])
        return None

    def get_available_events(self):
        result = []
        for row in self.db.get_available_events():
            result.append(Event.get_by_id(self.db, row[0]))

        return result

    def __str__(self):
        return f"{self.email}"


class Show:
    def __init__(
            self,
            db,
            event_id: int,
            name: str,
            start_time: datetime,
            end_time: datetime,
            price: Decimal,
            show_id: int = None
    ):
        self.db = db
        if show_id:
            self.show_id = show_id
            self.db.update_show(show_id, name, start_time, end_time, price)
        else:
            self.show_id = self.db.create_show(event_id, name, start_time, end_time, price)

        self.show_id, self.event_id, self._name, self._start_time, self._end_time, self._price \
            = self.db.get_show_by_id(self.show_id)

    def delete(self):
        self.db.delete_show(self.show_id)

    def update(self):
        self.db.update_show(self.show_id, self._name, self._start_time, self._end_time, self._price)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: datetime):
        self._name = new_name
        self.update()

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
        row = db.get_show_by_id(show_id)
        if row:
            return cls(db, row[1], row[2], row[3], row[4], row[5], row[0])
        return None

    def __str__(self):
        return f"{self.show_id}. {self._name} {self._start_time}-{self._end_time}"

    def list_item(self):
        return (f"{self.show_id}. {self._name} od {self._start_time.format("YYYY-MM-DD HH:mm")}"
                f" do {self._end_time.format("YYYY-MM-DD HH:mm")}, cena: {self._price}")


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
            self.event_id = self.db.create_event(name, event_type, creator_id)

        self.event_id, self._name, self.event_type, self.creator_id = self.db.get_event_by_id(self.event_id)

    def delete(self):
        self.db.delete_event(self.event_id)

    def update(self):
        self.db.update_event(self.event_id, self._name, self.event_type)

    @classmethod
    def get_by_id(cls, db, event_id):
        row = db.get_event_by_id(event_id)
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

    def delete_show(
            self,
            show: Show,
    ):
        show.delete()

    def create_show(
            self,
            name: str,
            start_time: datetime,
            end_time: datetime,
            price: Decimal,
    ) -> Show:
        return Show(self.db, self.event_id, name, start_time, end_time, price)

    def get_shows(self, requested_tickets=0):
        result = []

        if requested_tickets > 0:
            rows = self.db.get_shows_with_enough_tickets(self.event_id, requested_tickets)
        else:
            rows = self.db.get_shows_by_event_id(self.event_id)

        for row in rows:
            result.append(Show.get_by_id(self.db, row[0]))

        return result


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

        self.ticket_id, self.show_id, self.participant_id = self.db.get_ticket_by_id(self.ticket_id)

    def delete(self):
        self.db.delete_ticket(self.ticket_id)

    def update(self):
        self.db.update_ticket(self.ticket_id, self.participant_id)

    @classmethod
    def get_by_id(cls, db, ticket_id):
        row = db.get_ticket_by_id(ticket_id)
        if row:
            return cls(db, row[1], row[2], row[0])
        return None

    def cancel_ticket(self) -> None:
        self.delete()


class Participant(Person):
    def buy_ticket(self, show: Show) -> Ticket:
        return Ticket(self.db, show.show_id, self.person_id)

    def get_my_tickets(self):
        result = []
        for row in self.db.get_tickets(self.person_id):
            result.append((
                Ticket.get_by_id(self.db, row[0]),
                Event.get_by_id(self.db, row[1]),
                Show.get_by_id(self.db, row[2]),
            ))
        return result

    def __str__(self) -> str:
        """
        this is class str for present class object.
        :return: public information.
        """
        return f'{self.first_name} {self.last_name} [{self.email}]'


class EventCreator(Person):
    """Osoba odpowiedzialna za utworzenie wydarzenia"""

    def create_event(
            self,
            name: str,
            event_type: str,
    ) -> Event:
        return Event(self.db, name, event_type, self.person_id)

    def get_my_events(self):
        result = []
        for row in self.db.get_events_by_creator_id(self.person_id):
            result.append(Event.get_by_id(self.db, row[0]))

        return result

    def delete_event(
            self,
            event: Event,
    ) -> None:
        event.delete()
