import os
from classes import Event, Participant, EventCreator, Show, Ticket
from functions import get_list_from_json, make_test_jsons


if __name__ == '__main__':

    if not os.path.exists('jsons/*.json'):
        make_test_jsons()

    event_creator_list = get_list_from_json(EventCreator, 'jsons/EventCreator.json')
    EventCreator.set_id_counter(max(event_creator._id for event_creator in event_creator_list))

    event_list = get_list_from_json(Event, 'jsons/Event.json')
    Event.set_id_counter(max(event._id for event in event_list))

    participant_list = get_list_from_json(Participant, 'jsons/Participant.json')
    Participant.set_id_counter(max(participant._id for participant in participant_list))

    show_list = get_list_from_json(Show, 'jsons/Show.json')
    Show.set_id_counter(max(show._id for show in show_list))

    ticket_list = get_list_from_json(Ticket, 'jsons/Ticket.json')
    Ticket.set_id_counter(max(ticket._id for ticket in ticket_list))

    reception_desk_list = get_list_from_json(Reception_Desk, 'jsons/Reception_Desk')




    print(f"{event_list = }")
    print(f"{event_creator_list = }")
    print(f"{participant_list = }")
    print(f"{show_list = }")
    print(f"{ticket_list = }")


#custom_exception
class PasswordError(Exception):
    pass


class UsernameError(Exception):
    pass


class RegisterError(Exception):
    pass


class LoginError(Exception):
    pass
