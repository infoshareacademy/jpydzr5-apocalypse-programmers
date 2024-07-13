import pendulum
from classes import Event, Participant, EventCreator, Show, Ticket
from decimal import Decimal
from database import Database
from menu import main_menu


def fill_if_empty(db):
    event_creator1 = EventCreator.get_by_id(db, 1)
    if not event_creator1:
        event_creator1 = EventCreator(db, 'test1@example.com', 'password1')

    event_creator2 = EventCreator.get_by_id(db, 2)
    if not event_creator2:
        event_creator2 = EventCreator(db, 'test1@example.com', 'password1')

    event1 = Event.get_by_id(db, 1)
    if not event1:
        event1 = event_creator1.add_event('Dawid Podsiadło Na Żywo', 'koncert')

    event2 = Event.get_by_id(db, 2)
    if not event2:
        event2 = event_creator1.add_event('Andrea Bocelli', 'koncert')

    show1 = Show.get_by_id(db, 1)
    if not show1:
        show1 = event_creator1.add_show(
            event1,
            pendulum.datetime(2024, 8, 1, 18, 0),
            pendulum.datetime(2024, 8, 1, 20, 0),
            Decimal('120')
        )

    show2 = Show.get_by_id(db, 2)
    if not show2:
        show2 = event_creator2.add_show(
            event1,
            pendulum.datetime(2024, 8, 2, 18, 0),
            pendulum.datetime(2024, 8, 2, 20, 0),
            Decimal(120),
        )

    participant1 = Participant.get_by_id(db, 1)
    if not participant1:
        participant1 = Participant(db, 'client@example.com', 'passwordclient')

    ticket1 = Ticket.get_by_id(db, 1)
    if not ticket1:
        ticket1 = participant1.buy_ticket(show1)


if __name__ == '__main__':

    db = Database('ticket_system.db')

    fill_if_empty(db)

    main_menu(db)
