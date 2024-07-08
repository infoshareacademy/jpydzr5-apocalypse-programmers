"""module with classes"""
from datetime import datetime
import hashlib
from database_connection import DatabaseConnection
from exceptions import PasswordError, UsernameError, RegisterError, LoginError


class Event:
    """Przodek klas związanych z wydarzeniem"""

    def __init__(
            self,
            name: str,
            event_type: str,
            start_time: datetime,
            creator_id: int,
            event_id: int = None,
    ):
        self._name = name  # unikalny indentyfikator wydarzenia
        self.event_type = event_type
        self.start_time = start_time
        self.creator_id = creator_id  # relacja do osoby tworzącej wydarzenie
        self.event_id = event_id

    def save(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        if self.event_id is None:
            cursor.execute('''
                        INSERT INTO event (name, event_type, start_time, creator_id)
                        VALUES (?, ?, ?, ?)
                    ''', (self._name, self.event_type, self.start_time.to_iso8601_string(), self.creator_id))
            self.event_id = cursor.lastrowid
        else:
            cursor.execute('''
                        UPDATE event
                        SET name = ?, event_type = ?, start_time = ?
                        WHERE id = ?
                    ''', (self._name, self.event_type, self.start_time.to_iso8601_string(), self.event_id))
        conn.commit()

    @staticmethod
    def get_by_id(event_id):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, event_type, start_time, creator_id FROM event WHERE id = ?', (event_id,))
        row = cursor.fetchone()
        if row:
            return Event(row[1], row[2], row[3], row[4], row[0])
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

    @staticmethod
    def get_by_id(person_id):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, password FROM person WHERE id = ?', (person_id,))
        row = cursor.fetchone()
        if row:
            return Person(row[1], row[2], row[0])
        return None

    def __str__(self):
        return f"{self.email}"


class Show:

    def __init__(self, event_id, start_time, end_time, price, show_id: int = None ):
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
                    ''', (self.event_id, self.start_time.to_iso8601_string(), self.end_time.to_iso8601_string(), self.price))
            self.show_id= cursor.lastrowid
        else:
            cursor.execute('''
                        UPDATE show
                        SET start_time = ?, end_time = ?, price = ?
                        WHERE id = ?
                    ''', (self.start_time.to_iso8601_string(), self.end_time.to_iso8601_string(), self.price, self.show_id))
        conn.commit()

    @staticmethod
    def get_by_id(show_id):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, event_id, start_time, end_time, price FROM show WHERE id = ?', (show_id,))
        row = cursor.fetchone()
        if row:
            return Show(row[1], row[2], row[3], row[4], row[0])
        return None


    @classmethod
    def add_show(cls, event_id, start_time, end_time, price):
        show = cls(show_id, event_id, start_time, end_time, price)

    @classmethod
    def edit_show(cls, show_id, new_event_id, new_start_time, new_end_time,
                  new_price):
        cls.delete_show(show_id)
        show = cls(show_id, new_event_id, new_start_time, new_end_time, new_price)

    def delete_show(show_id: str) -> None:
        del dic[show_id]

    @staticmethod
    def show_which_show(event_id):
        # show = list((get_list_from_json).values())
        for show in show:
            if show['event_id'] == event_id:
                # show = get_list_from_json(show['show_id'])
                return f"({show['show_id']}) - |{show['start_time']} to {show['end_time']} \n      "\
                       f"|price : {show['price']}"
            else:
                raise ValueError('not found show for this event')


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
            self.ticket_id= cursor.lastrowid
        else:
            cursor.execute('''
                        UPDATE ticket
                        SET participant_id = ?
                        WHERE id = ?
                    ''', (self.participant_id, self.ticket_id))
        conn.commit()

    @staticmethod
    def get_by_id(ticket_id):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, show_id, participant_id FROM ticket WHERE id = ?', (ticket_id,))
        row = cursor.fetchone()
        if row:
            return Show(row[1], row[2], row[0])
        return None

    @classmethod
    def show_ticket(cls):
        # user = Participant._get_next_id()
        # show = Show._get_next_id()
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
        # dic = get_list_from_json()
        ticket_id = ticket['ticket_id']
        dic.update({ticket_id: ticket})
        try:
            with open("jsons/Ticket.json", "w") as fp:
                json.dump(dic, fp, indent=4)  # encode dict into JSON
        except Exception as ex:
            print('You have error', ex)

    @staticmethod
    def delete_ticket(ticket_id: str) -> None:
        # dic = get_list_from_json()
        del dic[ticket_id]

class Participant:

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
