"""module with classes"""
import copy
from datetime import datetime
import sqlite3
import pendulum
from tkinter import messagebox
import random
import string
import re
import hashlib

from functions import get_list_from_json
from main import PasswordError, UsernameError, RegisterError, LoginError


def show_message(title, message):
    """Pokazuje wiadomosci oraz bledy"""
    messagebox.showerror(title, message)


class Event:
    """Przodek klas związanych z wydarzeniem"""
    _id_counter = 0

    def __init__(
            self,
            id: int,
            name: str,
            event_type: str,
            start_time:datetime,
            creator_id: int,
    ):
        self._id = Event._get_next_id()
        self._name = name  # unikalny indentyfikator wydarzenia
        self.event_type = event_type
        self.start_time = start_time
        self.creator_id = creator_id  # relacja do osoby tworzącej wydarzenie

    @classmethod
    def _get_next_id(cls):
        cls._id_counter += 1
        return cls._id_counter

    @classmethod
    def set_id_counter(cls, new_max_id):
        cls._id_counter = new_max_id


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
    _id_counter = 0
    first_name: str = ''
    last_name: str = ''

    def __init__(
            self,
            id: int,
            email: str,
            password: str
    ):
        self._id = Person._get_next_id()
        self.email = email  # unikalny indentyfikator osoby
        self.password = password

    @classmethod
    def _get_next_id(cls):
        cls._id_counter += 1
        return cls._id_counter

    @classmethod
    def set_id_counter(cls, new_max_id):
        cls._id_counter = new_max_id

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


class Show:
    _id_counter = 0

    def __init__(self, show_id, event_id, start_time, end_time, price, datetime):
        self.show_id = Show._get_next_id()
        self.event_id = Event._get_next_id()
        self.start_time = start_time
        self.end_time = end_time
        self.price = price
        self.datetime = datetime

    @classmethod
    def _get_next_id(cls):
        cls._id_counter += 1
        return cls._id_counter

    @classmethod
    def set_id_counter(cls, new_max_id):
        cls._id_counter = new_max_id

    def get_show_database(self) -> dict:
        """
        gets database content
        :return: dictionary of user accounts
        """
        try:
            with open("jsons/Show.json", "r") as fp:
                # Load the dictionary from the file
                return json.load(fp)
        except Exception as ex:
            print('You have error in get database', ex)


    @classmethod
    def add_show(cls, event_id, start_time, end_time, price, datetime):
        show_id = Show._get_next_id()
        show = cls(show_id, event_id, start_time, end_time, price, datetime)
        cls.save_show(vars(show))

    @classmethod
    def edit_show(cls, show_id, new_event_id, new_start_time, new_end_time,
                  new_price, new_datetime):
        cls.delete_show(show_id)
        show = cls(show_id, new_event_id, new_start_time, new_end_time,
                      new_price, new_datetime)
        cls.save_show(vars(show))

    def save_show(show: dict) -> None:
        dic = get_list_from_json()
        show_id = Show._get_next_id()
        dic.update({show_id: show})
        try:
            with open("jsons/show.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)

    def delete_show(show_id: str) -> None:
        dic = get_list_from_json()
        del dic[show_id]
        try:
            with open("jsons/show.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)


    @staticmethod
    def show_which_show(event_id):
        show = list((get_list_from_json).values())
        for show in show:
            if show['event_id'] == event_id:
                show = get_list_from_json(show['show_id'])
                return f"({show['show_id']}) - |{show['start_time']} to {show['end_time']} \n      "\
                       f"|price : {show['price']}"
            else:
                raise ValueError('not found show for this event')


class Ticket:
    _id_counter = 0

    @classmethod
    def _get_next_id(cls):
        cls._id_counter += 1
        return cls._id_counter

    @classmethod
    def set_id_counter(cls, new_max_id):
        cls._id_counter = new_max_id

    def __init__(self, ticket_id, show_id, participant_id):
        self.ticket_id = Ticket._get_next_id(), ticket_id
        self.show_id = Show._get_next_id(), show_id
        self.participant_id = Participant._get_next_id(), participant_id

    @classmethod
    def show_ticket(cls):
        user = Participant._get_next_id()
        show = Show._get_next_id()
        if int(show['capacity']) >= 1:
            price = int(show['price'])
            final_price = price # can put here a tax
            if user['payment'] >= final_price:
                event_name = get_list_from_json(show['event_id'])['name']
                show_time = show['start_time'] + ' to ' + show['end_time']
                show_datetime = show['datetime']
                final_price = final_price
                return f' _________________________ Your Ticket __________________________\n'\
                      f'       event  : {event_name}\n'\
                      f'       date : {show_datetime}\n'\
                      f'       time : {show_time}\n'\
                      f'       final price : {final_price}\n'\
                      f' __________________________________________________________________'
            else:
                raise ValueError('Your payment is Not enough')
        else:
            raise ValueError("this show doesn't have capacity")


    @classmethod
    def buy_ticket(cls, participant, show_id, delete_show=None, save_show=None):
        show = Show._get_next_id()
        if int(show['capacity']) >= 1:
            price = int(show['price'])
            user = get_list_from_json(participant)
            final_price = price
            if user['payment'] >= final_price:
                ticket_id = Ticket._get_next_id()
                ticket = (ticket_id, show_id, participant)
                cls.save_ticket(vars(ticket))
                show['capacity'] = str(int(show['capacity']) - 1)
                delete_show(show_id)
                save_show(show)
            else:
                raise ValueError('Your wallet balance is Not enough')

    @staticmethod
    def save_ticket(ticket: dict) -> None:
        dic = get_list_from_json()
        ticket_id = ticket['ticket_id']
        dic.update({ticket_id: ticket})
        try:
            with open("jsons/Ticket.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)

    @staticmethod
    def delete_ticket(ticket_id: str) -> None:
        dic = get_list_from_json()
        del dic[ticket_id]
        try:
            with open("jsons/Ticket.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)


class Participant:
    _id_counter = 0


    def __init__(self, username: str, password: str, signup_datetime: str) -> None:

        """
        this is initializer for Participant class
        :param username: input username
        :param password: input password
        :param participant_id: generated auto participant_id
        """
        self.participant_id = Participant._get_next_id()
        self.username = username
        self.__password = password
        self.signup_datetime = signup_datetime

    @classmethod
    def _get_next_id(cls):
        cls._id_counter += 1
        return cls._id_counter

    @classmethod
    def set_id_counter(cls, new_max_id):
        cls._id_counter = new_max_id

        
    @staticmethod
    def validate_pass(password: str) -> None:
        """
        this method validate password
        :param password: password for check
        :return: None if password was correct. or rais error if not valid
        """
        if password == '' or password.isspace():
            raise PasswordError('\n--- your password was empty! you must set password ---\n')
        elif len(password) < 4:
            raise PasswordError('\n--- The length of the password must be more than 4 characters! ---\n')
        return None  # why wrong with false?

    @staticmethod
    def validate_username(username: str) -> None:
        """
        this method validate username
        :param username:
        :return:
        """
        if len(username) == 0:
            raise UsernameError('\n--- your username was empty! you must set password ---\n')
        return None # false?

    @staticmethod
    def build_pass(password: str) -> str:
        """
        this method hashed password by hashlib
        :param password:
        :return: hashed password
        """
        password = password.encode()
        p_hash = hashlib.sha256()
        p_hash.update(password)
        password = p_hash.hexdigest()
        return password
        # return password = hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def authenticated(cls, username: str) -> object | None:
        """
        this method check user is authenticated or not ...
        :param username: username
        :return: if authenticated return user object . if not, return None.
        """
        user = get_list_from_json(username)
        if user is not None:
            user = cls(user['username'], user['password'], user['signup_datetime'])
            return user
        else:
            return None

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
            signup_datetime = str(datetime.now())
            participant = Participant(username, password,  signup_datetime)
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

    def change_info(self, new_username: str, delete, save) -> None:
        """
        this method change username or phone number
        :param new_username: new participant-name
        """
        if self.validate_username(new_username):
            return self.validate_username(new_username)
        delete(self.username)
        self.username = new_username
        save(vars(self))

    def change_password(self, old: str, new: str, confirm_new: str, delete, save) -> None:
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



    def delete(username: str) -> None:
        """
        delete participant object from database
        :param username: username of participant account
        :return: None
        """
        dic = get_list_from_json()
        del dic[username]
        try:
            with open("jsons/Participant.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)

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
        participant_id, username = self.participant_id, self.username
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
