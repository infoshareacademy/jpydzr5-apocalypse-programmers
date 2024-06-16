"""module with classes"""
from datetime import datetime
import sqlite3
import pendulum
from tkinter import messagebox
import random
import string
import re

from functions import save_event, get_event_object, delete_event, get_event_database,\
    save_place, get_place_database,get_place_object,delete_place,\
    save_reception_desk, get_reception_desk_database,get_reception_desk_object, delete_reception_desk,\
    save_session, get_session_database, get_session_object, delete_session, \
    save_ticket, get_ticket_database, get_ticket_object, delete_ticket, \

def show_message(title, message):
    """Pokazuje wiadomosci oraz bledy"""
    messagebox.showerror(title, message)


def get_random_string(self):
    """generuje losowy oraz unikatowy id"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(8))

class Event:
    """Przodek klas związanych z wydarzeniem"""
    def __init__(
            self,
            id: int,
            name: str,
            event_type: str,
            start_time:datetime,
            creator_id: int,
    ):
        self._id = id  # zamienić na generator identyfikatorow, zeby nie bylo duplikatow
        self._name = name  # unikalny indentyfikator wydarzenia
        self.event_type = event_type
        self.start_time = start_time
        self.creator_id = creator_id  # relacja do osoby tworzącej wydarzenie


    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    def __str__(self):
        return f"{self._name}"

    def to_dict(self):
        result = vars(self).copy()  # Użyjemy kopii, aby nie modyfikować oryginalnego słownika
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        return result

    @staticmethod
    def from_dict(data):
        event = Event(0,'','',pendulum.now('Europe/Warsaw'),0)
        date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

        for key, value in data.items():
            if isinstance(value, str) and date_pattern.match(value):
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    pass
            setattr(event, key, value)

        return event

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

    def to_dict(self):
        result = vars(self).copy()  # Użyjemy kopii, aby nie modyfikować oryginalnego słownika
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        return result

    @staticmethod
    def from_dict(data):
        person = Person(0,'','')
        date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

        for key, value in data.items():
            if isinstance(value, str) and date_pattern.match(value):
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    pass
            setattr(person, key, value)

        return person

class Session:
    def __init__(self, session_id, event_id, place_id, reception_desk_id, start_time, end_time, price, datetime):
        self.session_id = session_id
        self.event_id = event_id
        self.place_id = place_id
        self.reception_desk_id = reception_desk_id
        self.start_time = start_time
        self.end_time = end_time
        self.price = price
        self.datetime = datetime
        self.reception_desk = get_reception_desk_object(reception_desk_id)
        self.capacity = reception_desk['seats_no']

    @classmethod
    def add_session(cls, event_id, place_id, reception_desk_id, start_time, end_time, price, datetime):
        session_id = cls.generate_id()
        session = cls(session_id, event_id, place_id, reception_desk_id, start_time, end_time, price, datetime)
        save_session(vars(session))

    @classmethod
    def edit_session(cls, session_id, new_event_id, new_place_id, new_reception_desk_id, new_start_time, new_end_time,
                     new_price, new_datetime):
        delete_session(session_id)
        session = cls(session_id, new_event_id, new_place_id, new_reception_desk_id, new_start_time, new_end_time,
                      new_price, new_datetime)
        save_session(vars(session))

    @staticmethod
    def delete_session(session_id):
        delete_session(session_id)

    @staticmethod
    def show_which_session(event_id, place_id, reception_desk_id):
        sessions = list(get_session_database().values())
        for session in sessions:
            if session['event_id'] == event_id and\
               session['place_id'] == place_id and\
               session['reception_desk_id'] == reception_desk_id:

                session = get_session_object(session['session_id'])
                return f"({session['session_id']}) - |{session['start_time']} to {session['end_time']} \n      "\
                       f"|capacity status : {session['capacity']} empty seats\n      "\
                       f"|price : {session['price']}"
            else:
                raise ValueError('not found session for this movie')

    @staticmethod
    def generate_id():
        dicti = get_session_database()
        try:
            last_id = max(list(map(int, list(dicti.keys()))))
            last_id += 1
        except:
            last_id = 1
        return str(last_id)



class Ticket:
    def __init__(self, ticket_id, session_id, participant):
        self.ticket_id = ticket_id
        self.session_id = session_id
        self.participant = participant

    @classmethod
    def show_ticket(cls, participant, session_id):
        user = get_object(participant)
        session = get_session_object(session_id)
        if int(session['capacity']) >= 1:
            price = int(session['price'])
            final_price = price # can put here a tax
            if user['payment'] >= final_price:
                event_name = get_event_object(session['event_id'])['name']
                placee_name = get_place_object(session['place_id'])['name']
                reception_desk_name = get_reception_desk_object(session['reception_desk_id'])['name']
                session_time = session['start_time'] + ' to ' + session['end_time']
                session_datetime = session['datetime']
                final_price = final_price
                return f' _________________________ Your Ticket __________________________\n'\
                      f'       event  : {event_name}\n'\
                      f'       place : {place_name}\n'\
                      f'       reception_desk  : {reception_desk_name} \n'\
                      f'       date : {session_datetime}\n'\
                      f'       time : {session_time}\n'\
                      f'       final price : {final_price}\n'\
                      f' __________________________________________________________________'
            else:
                raise ValueError('Your payment is Not enough')
        else:
            raise ValueError("this session doesn't have capacity")


    @classmethod
    def buy_ticket(cls, participant, session_id):
        session = get_session_object(session_id)
        if int(session['capacity']) >= 1:
            price = int(session['price'])
            user = get_object(participant)
            discount = cls.apply_discount(participant)
            final_price = price * (1-discount)
            if user['payment'] >= final_price:
                cls.payment(participant, final_price)
                ticket_id = cls.generate_id()
                ticket = cls(ticket_id, session_id, participant)
                save_ticket(vars(ticket))
                session['capacity'] = str(int(session['capacity']) - 1)
                delete_session(session_id)
                save_session(session)
            else:
                raise ValueError('Your wallet balance is Not enough')

    @staticmethod
    def generate_id():
        dicti = get_ticket_database()
        try:
            last_id = max(list(map(int,list(dicti.keys()))))
            last_id += 1
        except:
            last_id = 1
        return str(last_id)

class Participant(Person):
    """Uczestnik wydarzenia"""
    def show_events(
            self,
            name: str,
            event_type: str,
            start_time: datetime,
    ) -> Event:
        return Event(name, event_type, start_time)

    event_list = []

    for info in event_list:
        print(info.name, info.event_type, info.start_time)

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
                pass
            # show_message('Error', e)
            finally:
                pass
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
    ) -> Event:
        return Event(id, name, event_type, start_time, self._id)

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
