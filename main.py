import os
from classes import Event, Participant, EventCreator
from functions import get_list_from_json, make_test_jsons


if __name__ == '__main__':

    if not os.path.exists('jsons/*.json'):
        make_test_jsons()

    event_creator_list = get_list_from_json(EventCreator, 'jsons/EventCreator.json')
    event_list = get_list_from_json(Event, 'jsons/Event.json')
    participant_list = get_list_from_json(Participant, 'jsons/Participant.json')

    print(f"{event_list = }")
    print(f"{event_creator_list = }")
    print(f"{participant_list = }")


