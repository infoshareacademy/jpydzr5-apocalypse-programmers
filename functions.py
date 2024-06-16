from typing import List
from classes import EventCreator, Participant, Ticket
import pendulum
import os

import json

def get_list_from_json(cls: object, file_name: str):
    """wczytuje listę z pliku json"""
    if cls is None or not hasattr(cls, 'from_dict'):
        raise ValueError(f"No class named '{cls}' with a 'from_dict' method found")

    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
        return [cls.from_dict(item) for item in data]

def save_objects_to_json(filename: str, data: List) -> bool:
    """ zapisuje listę do pliku json

    metoda uniwersalna dla wszystkich obiektów"""
    data_as_dicts = [obj.to_dict() for obj in data]
    print(data_as_dicts)
    with open(filename, "w") as f:
        json.dump(data_as_dicts, f)


def make_test_jsons():
    """metoda do uruchomienia tylko raz, żeby stworzyć stosowne pliki

    Jak już wszystkie pliki json zostaną utworzone, to nie ma sensu już jej wykorzystywać"""
    file_path = 'jsons/EventCreator.json'

    if not os.path.exists(file_path):
        event_creator1 = EventCreator(1, 'event.creator@gmail.com', 'abcd')
        event_creator2 = EventCreator(2, 'event.creator@wp.pl', '1234')

        save_objects_to_json(
            file_path,
            [event_creator1, event_creator2, ],
        )

    file_path = 'jsons/Participant.json'

    if not os.path.exists(file_path):

        participant1 = Participant(1, 'participant1@gmail.com', 'abcd')
        participant2 = Participant(2, 'participant2@wp.pl', '1234')

        save_objects_to_json(
            file_path,
            [participant1, participant2, ],
        )

    file_path = 'jsons/Event.json'

    if not os.path.exists(file_path):
        save_objects_to_json(
            file_path,
             [event_creator1.add_event(1, 'Koncert Kult', 'Koncert',
                                           pendulum.datetime(2024, 10, 12, 19).in_timezone('Europe/Warsaw')),
                  event_creator1.add_event(2, 'Koncert Lady Gaga', 'Koncert',
                                           pendulum.datetime(2024, 7, 12, 19).in_timezone('Europe/Warsaw')),
                  event_creator2.add_event(3, 'Standup Abelard Giza', 'Stand-Up',
                                           pendulum.datetime(2024, 10, 1, 19).in_timezone('Europe/Warsaw')),
                  event_creator2.add_event(4, 'Standup Socha', 'Stand-Up',
                                           pendulum.datetime(2024, 10, 1, 19).in_timezone('Europe/Warsaw'))]
        )
    # @Maksym - tu dopisz swoje obiekty


#-----------------------------------------Place------------------------------------------


def get_place_database() -> dict:
    try:
        with open("Tickets_Session/json/place.json", "r") as fp:
            # Load the dictionary from the file
            return json.load(fp)
    except Exception as ex:
        print('You have error in get database', ex)


def save_place(place: dict) -> None:
    dic = get_place_database()
    place_id = place['place_id']
    dic.update({place_id: place})
    try:
        with open("Tickets_Session/json/place.json", "w") as fp:
            json.dump(dic, fp, indent=4)  # encode dict into JSON
    except Exception as ex:
        print('You have error', ex)


def delete_place(place_id: str) -> None:
    dic = get_place_database()
    del dic[place_id]
    try:
        with open("Tickets_Session/json/place.json", "w") as fp:
            json.dump(dic, fp, indent=4)  # encode dict into JSON
    except Exception as ex:
        print('You have error', ex)


def get_place_object(place_id: str) -> dict | None:
    try:
        with open("Tickets_Session/json/place.json", "r") as fp:
            # Load the dictionary from the file
            place_dict = json.load(fp)
            place = place_dict[place_id]
            return place
    except Exception:
        return None

#-----------------------------------------Event_Place_Reception_desk------------------------------------------


def get_event_database() -> dict:
    try:
        with open("Tickets_Session/json/event.json", "r") as fp:
            # Load the dictionary from the file
            return json.load(fp)
    except Exception as ex:
        print('You have error in get event-database', ex)


def save_event(event: dict) -> None:
    dic = get_event_database()
    event_id = event['event_id']
    dic.update({event_id: event})
    try:
        with open("Tickets_Session/json/event.json", "w") as fp:
            json.dump(dic, fp, indent=4)  # encode dict into JSON
    except Exception as ex:
        print('You have error', ex)


def delete_event(event_id: str) -> None:
    dic = get_event_database()
    del dic[event_id]
    try:
        with open("Tickets_Session/json/event.json", "w") as fp:
            json.dump(dic, fp, indent=4)  # encode dict into JSON
    except Exception as ex:
        print('You have error', ex)


def get_event_object(event_id: str) -> dict | None:
    """
    get object from database
    :param event_id: username
    :return: user object
    """
    try:
        with open("Tickets_Session/json/event.json", "r") as fp:
            # Load the dictionary from the file
            event_dict = json.load(fp)
            event = event_dict[event_id]
            return event
    except Exception:
        return None


#-----------------------------------------Reception desk------------------------------------------


def get_reception_desk_database() -> dict:
    try:
        with open("Tickets_Session/json/reception_desk.json", "r") as fp:
            # Load the dictionary from the file
            return json.load(fp)
    except Exception as ex:
        print('You have error in get database', ex)


def save_reception_desk(reception_desk: dict) -> None:
    dic = get_reception_desk_database()
    reception_desk_id = reception_desk['reception_desk_id']
    dic.update({reception_desk_id: reception_desk})
    try:
        with open("Tickets_Session/json/reception_desk.json", "w") as fp:
            json.dump(dic, fp, indent=4)  # encode dict into JSON
    except Exception as ex:
        print('You have error', ex)


def delete_reception_desk(reception_desk_id: str) -> None:
    dic = get_reception_desk_database()
    del dic[reception_desk_id]
    try:
        with open("Ticketś/json/reception_desk.json", "w") as fp:
            json.dump(dic, fp, indent=4)  # encode dict into JSON
    except Exception as ex:
        print('You have error', ex)


def get_reception_desk_object(reception_desk_id: str) -> dict | None:
    try:
        with open("Tickets_Session/json/reception_desk.json", "r") as fp:
            # Load the dictionary from the file
            reception_desk_dict = json.load(fp)
            reception_desk = reception_desk_dict[reception_desk_id]
            return reception_desk
    except Exception:
        return None

#-----------------------------------------Session------------------------------------------


def get_session_database() -> dict:
    """
    gets database content
    :return: dictionary of user accounts
    """
    try:
        with open("Tickets_Session/json/session.json", "r") as fp:
            # Load the dictionary from the file
            return json.load(fp)
    except Exception as ex:
        print('You have error in get database', ex)


def save_session(session: dict) -> None:
    dic = get_session_database()
    session_id = session['session_id']
    dic.update({session_id: session})
    try:
        with open("Tickets_Session/json/session.json", "w") as fp:
            json.dump(dic, fp, indent=4)  # encode dict into JSON
    except Exception as ex:
        print('You have error', ex)


def delete_session(session_id: str) -> None:
    dic = get_session_database()
    del dic[session_id]
    try:
        with open("Tickets_Session/json/session.json", "w") as fp:
            json.dump(dic, fp, indent=4)  # encode dict into JSON
    except Exception as ex:
        print('You have error', ex)


def get_session_object(session_id: str) -> dict | None:
    try:
        with open("Tickets_Session/json/session.json", "r") as fp:
            # Load the dictionary from the file
            season_dict = json.load(fp)
            season = season_dict[session_id]
            return season
    except Exception:
        return None


#-----------------------------------------Ticket------------------------------------------


def get_ticket_database() -> dict:
    try:
        with open("Tickets_Session/json/ticket.json", "r") as fp:
            # Load the dictionary from the file
            return json.load(fp)
    except Exception as ex:
        print('You have error in get database', ex)


def save_ticket(ticket: dict) -> None:
    dic = get_ticket_database()
    ticket_id = ticket['ticket_id']
    dic.update({ticket_id: ticket})
    try:
        with open("Tickets_Session/json/ticket.json", "w") as fp:
            json.dump(dic, fp, indent=4)  # encode dict into JSON
    except Exception as ex:
        print('You have error', ex)


def delete_ticket(ticket_id: str) -> None:
    dic = get_ticket_database()
    del dic[ticket_id]
    try:
        with open("Tickets_Session/json/ticket.json", "w") as fp:
            json.dump(dic, fp, indent=4)  # encode dict into JSON
    except Exception as ex:
        print('You have error', ex)


def get_ticket_object(ticket_id: str) -> dict | None:
    try:
        with open("Tickets_Session/json/ticket.json", "r") as fp:
            # Load the dictionary from the file
            ticket_dict = json.load(fp)
            ticket = ticket_dict[ticket_id]
            return ticket
    except Exception:
        return None
