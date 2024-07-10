from decimal import Decimal

import pendulum
from classes import Event, Participant, EventCreator, Show, Ticket


if __name__ == '__main__':

    event_creator1 = EventCreator.get_by_id(1)
    if not event_creator1:
        event_creator1 = EventCreator('test1@example.com', 'password1')
        event_creator1.save()

    event_creator2 = EventCreator.get_by_id(2)
    if not event_creator2:
        event_creator2 = EventCreator('test1@example.com', 'password1')
        event_creator2.save()

    event1 = Event.get_by_id(1)
    if not event1:
        event1 = event_creator1.add_event('Dawid Podsiadło Na Żywo', 'koncert')
        event1.save()

    show1 = Show.get_by_id(1)
    if not show1:
        show1 = event_creator1.add_show(
            event1,
            pendulum.datetime(2024, 8, 1, 18, 0),
            pendulum.datetime(2024, 8, 1, 20, 0),
            Decimal('120')
        )
        show1.save()

    show2 = Show.get_by_id(2)
    if not show2:
        show2 = event_creator2.add_show(
            event1,
            pendulum.datetime(2024, 8, 2, 18, 0),
            pendulum.datetime(2024, 8, 2, 20, 0),
            Decimal(120),
        )
        show2.save()

    participant1 = Participant.get_by_id(1)
    if not participant1:
        participant1 = Participant('client@example.com', 'passwordclient')
        participant1.save()

    ticket1 = Ticket.get_by_id(1)
    if not ticket1:
        ticket1 = participant1.buy_ticket(show1)
