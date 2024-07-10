"""module with classes"""
from datetime import datetime
from decimal import Decimal
from database_connection import DatabaseConnection


class Event:
    """Przodek klas związanych z wydarzeniem"""
    event_id: int = None

    def __init__(
            self,
            name: str,
            event_type: str,
            creator_id: int,
            event_id: int = None,
    ):
        self._name = name  # unikalny indentyfikator wydarzenia
        self.event_type = event_type
        self.creator_id = creator_id  # relacja do osoby tworzącej wydarzenie
        self.event_id = event_id

    def save(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        if self.event_id is None:
            cursor.execute('''
                        INSERT INTO event (name, event_type, creator_id)
                        VALUES (?, ?, ?)
                    ''', (self._name, self.event_type, self.creator_id))
            self.event_id = cursor.lastrowid
        else:
            cursor.execute('''
                        UPDATE event
                        SET name = ?, event_type = ?
                        WHERE id = ?
                    ''', (self._name, self.event_type, self.event_id))
        conn.commit()

    def delete(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute('''
                        DELETE FROM event
                        WHERE id = ?
                    ''', (self.event_id,))
        conn.commit()

    @classmethod
    def get_by_id(cls, event_id):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, event_type, creator_id FROM event WHERE id = ?', (event_id,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[0])
        return None

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
    person_id: int = None
    first_name: str = ''
    last_name: str = ''

    def __init__(
            self,
            email: str,
            password: str,
            person_id: int = None,
    ):
        self.email = email  # unikalny indentyfikator osoby
        self.__password = password
        self.person_id = person_id

    def save(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        if self.person_id is None:
            cursor.execute('''
                        INSERT INTO person (email, password)
                        VALUES (?, ?)
                    ''', (self.email, self.__password))
            self.person_id = cursor.lastrowid
        else:
            cursor.execute('''
                        UPDATE person
                        SET email = ?, password = ?
                        WHERE id = ?
                    ''', (self.email, self.__password, self.person_id))
        conn.commit()

    def delete(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute('''
                        DELETE FROM person
                        WHERE id = ?
                    ''', (self.person_id,))
        conn.commit()

    @classmethod
    def get_by_id(cls, person_id):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, password FROM person WHERE id = ?', (person_id,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], row[0])
        return None

    def change_email(self, new_email):
        self.email = new_email
        self.save()

    def change_password(self, new_password):
        self.__password = new_password
        self.save()

    def match_pass(self, test_password: str) -> bool:
        """passwords matching
        """
        if self.__password == test_password:
            return True
        return False

    def __str__(self):
        return f"{self.email}"


class Show:

    def __init__(self, event_id, start_time, end_time, price, show_id: int = None):
        self.event_id = event_id
        self.start_time = start_time
        self.end_time = end_time
        self.price = price
        self.show_id = show_id

    def save(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        if self.show_id is None:
            cursor.execute('''
                        INSERT INTO show (event_id, start_time, end_time, price)
                        VALUES (?, ?, ?, ?)
                    ''', (
                self.event_id,
                self.start_time.to_iso8601_string(),
                self.end_time.to_iso8601_string(),
                str(self.price)
            ))
            self.show_id = cursor.lastrowid
        else:
            cursor.execute('''
                        UPDATE show
                        SET start_time = ?, end_time = ?, price = ?
                        WHERE id = ?
                    ''', (
                self.start_time.to_iso8601_string(),
                self.end_time.to_iso8601_string(),
                str(self.price),
                self.show_id
            ))
        conn.commit()

    def delete(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute('''
                        DELETE FROM show
                        WHERE id = ?
                    ''', (self.show_id,))
        conn.commit()

    @classmethod
    def get_by_id(cls, show_id):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, event_id, start_time, end_time, price FROM show WHERE id = ?', (show_id,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[0])
        return None


class Ticket:
    def __init__(self, show_id, participant_id, ticket_id: int = None):
        self.show_id = show_id
        self.participant_id = participant_id
        self.ticket_id = ticket_id

    def save(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        if self.ticket_id is None:
            cursor.execute('''
                        INSERT INTO ticket (show_id, participant_id)
                        VALUES (?, ?)
                    ''', (self.show_id, self.participant_id))
            self.ticket_id = cursor.lastrowid
        else:
            cursor.execute('''
                        UPDATE ticket
                        SET participant_id = ?
                        WHERE id = ?
                    ''', (self.participant_id, self.ticket_id,))
        conn.commit()

    def delete(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute('''
                        DELETE FROM ticket
                        WHERE id = ?
                    ''', (self.ticket_id,))
        conn.commit()

    @classmethod
    def get_by_id(cls, ticket_id):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, show_id, participant_id FROM ticket WHERE id = ?', (ticket_id,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], row[0])
        return None

    def cancel_ticket(self) -> None:
        self.delete()


class Participant(Person):
    def buy_ticket(self, show: Show) -> Ticket:
        ticket = Ticket(show.show_id, self.person_id)
        ticket.save()
        return ticket

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
        event = Event(name, event_type, self.person_id)
        event.save()
        return event

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
        event.save()

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
        show = Show(event.event_id, start_time, end_time, price)
        show.save()
        return show
