import pendulum
from classes import Event, Participant, EventCreator, Show, Ticket


if __name__ == '__main__':
    event_creator1 = EventCreator.get_by_id(1)
    event_creator2 = EventCreator.get_by_id(2)
    event1 = Event.get_by_id(1)

    show1 = Show(1, pendulum.datetime(2024,8,1,18,0), pendulum.datetime(2024, 8,1,20,0),120,1)
    show1.save()
    show2 = Show(1, pendulum.datetime(2024, 8, 2, 18, 0), pendulum.datetime(2024, 8, 2, 20, 0), 120, 1)
    show2.save()


    print(event1)



