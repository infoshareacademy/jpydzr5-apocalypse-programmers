from classes import EventCreator, Event, Participant, Ticket
from functions import save_objects_to_json
import pendulum


if __name__ == '__main__':
    event_creator1 = EventCreator(1, 'event.creator@gmail.com', 'abcd')
    event_creator2 = EventCreator(2, 'event.creator@wp.pl', '1234')

    event_creator_list = [event_creator1, event_creator2, ]

    save_objects_to_json(event_creator_list, 'jsons/event_creator_list.json')

    participant1 = Participant(1, 'participant1@gmail.com', 'abcd')
    participant2 = Participant(2, 'participant2@wp.pl', '1234')

    participant_list = [participant1, participant2, ]

    save_objects_to_json(participant_list, 'jsons/participant_list.json')

    event_list = []
    event_list.append(event_creator1.add_event(1, 'Koncert Kult', 'Koncert',
                                               pendulum.datetime(2024,10,12,19).in_timezone('Europe/Warsaw')))
    event_list.append(event_creator1.add_event(2, 'Koncert Lady Gaga', 'Koncert',
                                               pendulum.datetime(2024, 7, 12, 19).in_timezone('Europe/Warsaw')))

    event_list.append(event_creator2.add_event(3, 'Standup Abelard Giza', 'Stand-Up',
                                               pendulum.datetime(2024, 10, 1, 19).in_timezone('Europe/Warsaw')))

    event_list.append(event_creator2.add_event(4, 'Standup Socha', 'Stand-Up',
                                               pendulum.datetime(2024, 10, 1, 19).in_timezone('Europe/Warsaw')))

    save_objects_to_json(event_list, 'jsons/event_list.json')

