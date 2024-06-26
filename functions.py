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


