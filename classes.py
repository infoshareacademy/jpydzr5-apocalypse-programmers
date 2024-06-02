"""module with classes"""
from datetime import datetime
import sqlite3
from functions import show_message, get_random_string


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




class Ticket:
    """Daje Id biletom"""
    tickets = []
    for i in tickets:
        tickets.append(i)

    def __init__(
            self,
            id: int,
            event_name: str,
            participant_id: int,
            row: str,
            place: str
    ):
        """Pojedynczy bilet"""
        super().__init__(self)
        self._id = id  # zamienić na generator identyfikatorow, zeby nie bylo duplikatow
        self.event_name = event_name  # relacja do wydarzenia
        self.participant_id = participant_id  # relacja do uczestnika
        self.row = row
        self.place = place


class Participant(Person):
    """Uczestnik wydarzenia"""
    def show_events(
            self,
            name: str,
            event_type: str,
            start_time: datetime,
            end_time: datetime
    ) -> Event:
        return Event(name, event_type, start_time, end_time)

    event_list = []

    for info in event_list:
        print(info.name, info.event_type, info.start_time, info.end_time)

    def buy_ticket(self):
        while True:
            global tickets_id
            t_id = get_random_string()
            if t_id not in tickets_id:
                ticket_id.set(get_random_string())
                break
            continue

        def buy_ticket_now():
            if len(name.get()) < 5 or len(ticket_date.get()) < 7 or len(ticket_validity.get()) < 7:
                show_message('Error', 'Enter valid details')
                return
            try:
                """pobiera dane z bazy"""
                # conn = sqlite3.connect("ticket_booking_database.db")
                # cursor = conn.cursor()
                # cursor.execute("INSERT INTO ticket (name, ticket_id, ticket_date, ticket_validity) VALUES (?, ?, ?, ?)", (str(name.get()), str(ticket_id.get()), str(ticket_date.get()), str(ticket_validity.get())))
                # conn.commit()
                # show_message('Successful', 'Your booking is successful, your ticket id is {}'.format(ticket_id.get()))
                # top1.destroy()
            except sqlite3.Error as e:
            # show_message('Error', e)
            finally:
        # conn.close()

    def return_ticket(
            self,
            ticket: Ticket,
    ) -> None:
        del Ticket

        def delete_rows(ticket_id):
            try:
                conn = sqlite3.connect("ticket_booking_database.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ticket WHERE ticket_id = ?", (ticket_id,))
                conn.commit()
                show_message('Success', 'Ticket deleted')
                conn.close()
            except sqlite3.Error as e:
                show_message('Sqlite error', e)
            finally:
                conn.close()

        conn = sqlite3.connect('ticket_booking_database.db')
        cursor = conn.cursor()

    def show_my_tickets(self):
        conn = sqlite3.connect('ticket_booking_database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM ticket')
        tickets = cursor.fetchall()
        for i in range(len(tickets)):
        #    """podaje przyklad jak sam mam:"""
        #    """Label(top2, text=tickets[i][0], borderwidth=1, relief="solid", width=20).grid(row=i + 1, column=0)
        #    Label(top2, text=tickets[i][1], borderwidth=1, relief="solid", width=20).grid(row=i + 1, padx=10, column=1)
        #    Label(top2, text=tickets[i][2], borderwidth=1, relief="solid", width=20).grid(row=i + 1, padx=10, column=2)
        #    Label(top2, text=tickets[i][3], borderwidth=1, relief="solid", width=20).grid(row=i + 1, padx=10, column=3)"""
        #    """
            top2.mainloop()
            conn.close()



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
