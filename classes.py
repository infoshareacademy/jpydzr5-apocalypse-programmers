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

class Participant:
    def __init__(self, username: str, password: str, participant_id: str, signup_datetime: str) -> None:

        """
        this is initializer for Participant class
        :param username: input username
        :param password: input password
        :param participant_id: generated auto participant_id
        """
        self.participant_id = participant_id
        self.username = username
        self.__password = password
        self.signup_datetime = signup_datetime

    @classmethod
    def create_user(cls, username: str, password: str) -> 'Participant':
        """
        this method create user and save to database
        :param username: input username
        :param password: input password
        :param participant_id: participant_id
        """
        if Participant.validate_pass(password): # these are never can be true
            return cls.validate_pass(password) #this line never runs
        elif Participant.validate_username(username): ####
            return cls.validate_username(username) #####
        elif Participant.authenticated(username):
            raise RegisterError('\n--- Registration failed , This username already exist! ---\n')
        else:
            password = cls.build_pass(password)
            participant_id = str(uuid.uuid4())
            signup_datetime = str(datetime.now())
            participant = Participant(username, password, participant_id, signup_datetime)
            save(vars(participant))
            return participant


    @classmethod
    def login(cls, username: str, password: str) -> object:
        """
        this method login participant
        :param username: input username
        :param password: input password
        :return: participant object if is authenticated
        """
        hashed_password = cls.build_pass(password)
        participant = Participant.authenticated(username)
        if participant:
            if participant._Participant__password == hashed_password:
                return participant
            else:
                raise PasswordError('--- incorrect password ---')
        else:
            raise LoginError(f" --- There is no account with this username : {username} ---\n"
                             f" --- Please register and try again. ---")

    def change_info(self, new_username: str) -> None:
        """
        this method change username or phone number
        :param new_username: new participant-name
        """
        if self.validate_username(new_username):
            return self.validate_username(new_username)
        delete(self.username)
        self.username = new_username
        save(vars(self))

    def change_password(self, old: str, new: str, confirm_new: str) -> None:
        """
        change password participant
        :param old: old password
        :param new: new password
        :param confirm_new: confirm new password
        """
        old = self.build_pass(old)
        if old == self._Participant__password:
            if self.match_pass(new, confirm_new):
                if self.validate_pass(new) is None:
                    new = self.build_pass(new)
                    delete(self.username)
                    self.__password = new
                    save(vars(self))
                return self.validate_pass(new)
            else:
                raise PasswordError('--- new password and confirm password not mach ---')
        else:
            raise PasswordError('--- your old is invalid ---')

    @staticmethod
    def match_pass(p1: str, p2: str) -> bool:
        """
        passwords matching
        :param p1: password
        :param p2: confirm password
        :return: True if matched. return False if not matched.
        """
        if p1 == p2:
            return True
        return False

    def __str__(self) -> str:
        """
        this is class str for present class object.
        :return: public information.
        """
        participant_id, username, phone_number = self.participant_id, self.username
        return f'\nID = {participant_id}\n' \
               f'Username = {username}\n' \
               f'Sign up Date = {self.signup_datetime}\n' \



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
