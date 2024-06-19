"""module with classes"""
import copy
from datetime import datetime
import sqlite3
import pendulum
from tkinter import messagebox
import random
import string
import re

from functions import get_list_from_json, save_objects_to_json


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

    def __init__(self, show_id, event_id, place_id, reception_desk_id, start_time, end_time, price, datetime):
        self.show_id = Show._get_next_id()
        self.event_id = Event._get_next_id()
        self.place_id = place_id
        self.reception_desk_id = reception_desk_id
        self.start_time = start_time
        self.end_time = end_time
        self.price = price
        self.datetime = datetime
        self.reception_desk = get_reception_desk_object(reception_desk_id)
        self.capacity = reception_desk['seats_no']

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
    def add_show(cls, event_id, place_id, reception_desk_id, start_time, end_time, price, datetime):
        show_id = Show._get_next_id()
        show = cls(show_id, event_id, place_id, reception_desk_id, start_time, end_time, price, datetime)
        cls.save_show(vars(show))

    @classmethod
    def edit_show(cls, show_id, new_event_id, new_place_id, new_reception_desk_id, new_start_time, new_end_time,
                  new_price, new_datetime):
        cls.delete_show(show_id)
        show = cls(show_id, new_event_id, new_place_id, new_reception_desk_id, new_start_time, new_end_time,
                      new_price, new_datetime)
        cls.save_show(vars(show))

    def save_show(show: dict) -> None:
        dic = dict.get_show_database()
        show_id = Show._get_next_id()
        dic.update({show_id: show})
        try:
            with open("jsons/show.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)

    def delete_show(show_id):
        dic = ()
        del dic[show_id]
        try:
            with open("jsons/show.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)


    @staticmethod
    def show_which_show(event_id, place_id, reception_desk_id):
        show = list(().values())
        for show in show:
            if show['event_id'] == event_id and\
               show['place_id'] == place_id and\
               show['reception_desk_id'] == reception_desk_id:

                show = dict.get_show_database(show['show_id'])
                return f"({show['show_id']}) - |{show['start_time']} to {show['end_time']} \n      "\
                       f"|capacity status : {show['capacity']} empty seats\n      "\
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
        self.ticket_id = Ticket._get_next_id()
        self.show_id = Show._get_next_id()
        self.participant_id = Participant._get_next_id()


    def get_ticket_database(self) -> dict:
        try:
            with open("jsons/Ticket.json", "r") as fp:
                # Load the dictionary from the file
                return json.load(fp)
        except Exception as ex:
            print('You have error in get database', ex)

    @classmethod
    def show_ticket(cls, participant, show_id):
        user = Participant._get_next_id()
        show = Show._get_next_id()
        if int(show['capacity']) >= 1:
            price = int(show['price'])
            final_price = price # can put here a tax
            if user['payment'] >= final_price:
                event_name = get_event_object(show['event_id'])['name']
                place_name = get_place_object(show['place_id'])['name']
                reception_desk_name = get_reception_desk_object(show['reception_desk_id'])['name']
                show_time = show['start_time'] + ' to ' + show['end_time']
                show_datetime = show['datetime']
                final_price = final_price
                return f' _________________________ Your Ticket __________________________\n'\
                      f'       event  : {event_name}\n'\
                      f'       place : {place_name}\n'\
                      f'       reception_desk  : {reception_desk_name} \n'\
                      f'       date : {show_datetime}\n'\
                      f'       time : {show_time}\n'\
                      f'       final price : {final_price}\n'\
                      f' __________________________________________________________________'
            else:
                raise ValueError('Your payment is Not enough')
        else:
            raise ValueError("this show doesn't have capacity")


    @classmethod
    def buy_ticket(cls, participant, show_id):
        show = Show._get_next_id()
        if int(show['capacity']) >= 1:
            price = int(show['price'])
            user = get_object(participant)
            discount = cls.apply_discount(participant)
            final_price = price * (1-discount)
            if user['payment'] >= final_price:
                cls.payment(participant, final_price)
                ticket_id = cls.generate_id()
                ticket = cls(ticket_id, show_id, participant)
                save_ticket(vars(ticket))
                show['capacity'] = str(int(show['capacity']) - 1)
                delete_show(show_id)
                save_show(show)
            else:
                raise ValueError('Your wallet balance is Not enough')

    @staticmethod
    def save_ticket(ticket: dict) -> None:
        dic = dict.get_ticket_database()
        ticket_id = ticket['ticket_id']
        dic.update({ticket_id: ticket})
        try:
            with open("jsons/Ticket.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)

    @staticmethod
    def delete_ticket(ticket_id: str) -> None:
        dic = dict.get_ticket_database()
        del dic[ticket_id]
        try:
            with open("jsons/Ticket.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)



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

    def save(participant: dict) -> None:
        """
        save object in database
        :param participant: participant object
        :return: None
        """
        dic = get_database()
        username = participant['username']
        dic.update({username: participant})
        try:
            with open("jsons/Participant.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)

    def delete(username: str) -> None:
        """
        delete participant object from database
        :param username: username of participant account
        :return: None
        """
        dic = get_database()
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
