import os
from classes import Event, Participant, EventCreator
from functions import get_list_from_json, make_test_jsons


if __name__ == '__main__':

    if not os.path.exists('jsons/*.json'):
        make_test_jsons()

    event_creator_list = get_list_from_json(EventCreator, 'jsons/EventCreator.json')
    event_list = get_list_from_json(Event, 'jsons/Event.json')
    participant_list = get_list_from_json(Participant, 'jsons/Participant.json')
    show_list = get_list_from_json(Show, 'jsons/Show.json')
    reception_desk_list = get_list_from_json(Reception_Desk, 'jsons/Reception_Desk')




    print(f"{event_list = }")
    print(f"{event_creator_list = }")
    print(f"{participant_list = }")



#custom_exception
class PasswordError(Exception):
    pass


class UsernameError(Exception):
    pass


class RegisterError(Exception):
    pass


class LoginError(Exception):
    pass
