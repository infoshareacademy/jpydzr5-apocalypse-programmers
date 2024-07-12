from classes import EventCreator, Participant, Event, Show, Ticket
from datetime import datetime
from decimal import Decimal

# Przykładowy obiekt EventCreator i Participant
event_creator = EventCreator('Pawel', 'Lom', 'event.creator@gmail.com', 'password')
participant = Participant('Jan', 'Kowal', 'participant@gmail.com', 'password')

def event_creator_menu():
    options = {
        '1': ("Stwórz wydarzenie", add_event),
        '2': ("Edytuj wydarzenie", edit_event),
        '3': ("Usuń wydarzenie", del_event),
        '0': ("Wyjdź", exit)
    }
    menu("EventCreatora", options)

def participant_menu():
    options = {
        '1': ("Kup bilet", buy_ticket),
        '2': ("Zwróć bilet", return_ticket),
        '3': ("Pokaż moje bilety", show_my_tickets),
        '0': ("Wyjdź", exit)
    }
    menu("Participant", options)

def show_menu():
    options = {
        '1': ("Stwórz pokaz", add_show),
        '2': ("Skasuj pokaz", del_show),
        '0': ("Wyjdź", exit)
    }
    menu("Show", options)

def menu(title, options):
    while True:
        print(f"\n--- Menu {title} ---")
        for key, (description, _) in options.items():
            print(f"{key}. {description}")
        choice = input("Wybierz opcję: ")
        if choice in options:
            options[choice][1]()
        else:
            print("Niepoprawny wybór, spróbuj ponownie.")

# Implementacja funkcji wywoływanych w menu
def add_event():
    name = input("Podaj nazwę wydarzenia: ")
    event_type = input("Podaj typ wydarzenia: ")
    event_creator.add_event(name, event_type)
    print("Wydarzenie utworzone.")

def edit_event():
    event_id = int(input("Podaj ID wydarzenia do edycji: "))
    event = Event.get_by_id(event_id)
    if event:
        new_name = input("Podaj nową nazwę wydarzenia: ")
        event_creator.rename_event(event, new_name)
        print("Wydarzenie zaktualizowane.")
    else:
        print("Nie znaleziono wydarzenia.")

def del_event():
    event_id = int(input("Podaj ID wydarzenia do usunięcia: "))
    event = Event.get_by_id(event_id)
    if event:
        event_creator.del_event(event)
        print("Wydarzenie usunięte.")
    else:
        print("Nie znaleziono wydarzenia.")

def buy_ticket():
    show_id = int(input("Podaj ID pokazu: "))
    show = Show.get_by_id(show_id)
    if show:
        ticket = participant.buy_ticket(show)
        print("Bilet kupiony.")
    else:
        print("Nie znaleziono pokazu.")

def return_ticket():
    ticket_id = int(input("Podaj ID biletu do zwrotu: "))
    ticket = Ticket.get_by_id(ticket_id)
    if ticket:
        ticket.cancel_ticket()
        print("Bilet zwrócony.")
    else:
        print("Nie znaleziono biletu.")

def show_my_tickets():
    print("Wyświetlanie moich biletów... (do zaimplementowania)")

def add_show():
    event_id = int(input("Podaj ID wydarzenia: "))
    event = Event.get_by_id(event_id)
    if event:
        start_time = datetime.strptime(input("Podaj czas rozpoczęcia (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(input("Podaj czas zakończenia (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
        price = Decimal(input("Podaj cenę biletu: "))
        event_creator.add_show(event, start_time, end_time, price)
        print("Pokaz utworzony.")
    else:
        print("Nie znaleziono wydarzenia.")

def del_show():
    show_id = int(input("Podaj ID pokazu do usunięcia: "))
    show = Show.get_by_id(show_id)
    if show:
        event_creator.del_show(show)
        print("Pokaz usunięty.")
    else:
        print("Nie znaleziono pokazu.")

# Uruchomienie menu EventCreatora
if __name__ == "__main__":
    event_creator_menu()
