from functions import load_from_json



if __name__ == '__main__':

    event_creator_list = load_from_json(EventCreator, 'jsons/event_creator_list.json')
    event_list = load_from_json(Event, 'jsons/event_list.json')
    participant_list = load_from_json(Participant, 'jsons/participant.json')

