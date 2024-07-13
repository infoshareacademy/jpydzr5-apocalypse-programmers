import pendulum
from decimal import Decimal
from classes import EventCreator, Participant, Event, Show, Ticket


# Ogólna funkcja menu dla powtarzających się opcji
def menu(title, options):
    while True:
        print(f"\n--- Menu {title} ---")
        for key, (description, _) in options.items():
            if key == '0':
                print('')
            print(f"{key}. {description}")
        choice = input("\nWybierz opcję: ")
        if choice in options:
            options[choice][1]()
        else:
            print("Niepoprawny wybór, spróbuj ponownie.")


def create_event(event_creator):
    print("Tworzenie wydarzenia...")
    print("=" * 10)
    name = input('Podaj nazwę wydarzenia: ')
    event_type = input('Podaj typ wydarzenia (np. Koncert, Standup): ')
    event_creator.add_event(name, event_type)
    print("Wydarzenie utworzone.")


def edit_event(event_creator):
    print("Edycja wydarzenia...")
    event_id = int(input("Podaj ID wydarzenia do edycji: "))
    event = Event.get_by_id(event_id)
    if event:
        new_name = input("Podaj nową nazwę wydarzenia: ")
        event_creator.rename_event(event, new_name)
        print("Wydarzenie zaktualizowane.")
    else:
        print("Nie znaleziono wydarzenia.")


def delete_event(event_creator):
    print("Usuwanie wydarzenia...")
    event_id = int(input("Podaj ID wydarzenia do usunięcia: "))
    event = Event.get_by_id(event_id)
    if event:
        event_creator.del_event(event)
        print("Wydarzenie usunięte.")
    else:
        print("Nie znaleziono wydarzenia.")


def duplicate_event(event_creator): print("Powielanie wydarzenia...")


def show_events(event_creator):
    print("Wyświetlanie listy wydarzeń...")
    print("=" * 10)
    events = event_creator.get_my_events()
    for event in events:
        print(f"{event.event_id}. {event.name} ({event.event_type})")


def buy_ticket(db, participant):
    print("Kupowanie biletu...")
    show_id = int(input("Podaj ID pokazu: "))
    show = Show.get_by_id(show_id)
    if show:
        ticket = participant.buy_ticket(show)
        print("Bilet kupiony.")
    else:
        print("Nie znaleziono pokazu.")


def return_ticket(db, participant):
    print("Zwracanie biletu...")
    ticket_id = int(input("Podaj ID biletu do zwrotu: "))
    ticket = Ticket.get_by_id(ticket_id)
    if ticket:
        ticket.cancel_ticket()
        print("Bilet zwrócony.")
    else:
        print("Nie znaleziono biletu.")


def show_my_tickets(db):
    print("Wyświetlanie moich biletów... (do zaimplementowania)")


def create_show(db, event_creator):
    print("Tworzenie pokazu...")
    event_id = int(input("Podaj ID wydarzenia: "))
    event = Event.get_by_id(event_id)
    if event:
        start_time = pendulum.parse(input("Podaj czas rozpoczęcia (YYYY-MM-DD HH:MM): "))
        end_time = pendulum.parse(input("Podaj czas zakończenia (YYYY-MM-DD HH:MM): "))
        price = Decimal(input("Podaj cenę biletu: "))
        event_creator.add_show(event, start_time, end_time, price)
        print("Pokaz utworzony.")
    else:
        print("Nie znaleziono wydarzenia.")


def edit_show(db): print("Edycja pokazu...")


def delete_show(db, event_creator):
    print("Usuwanie pokazu...")
    show_id = int(input("Podaj ID pokazu do usunięcia: "))
    show = Show.get_by_id(show_id)
    if show:
        event_creator.del_show(show)
        print("Pokaz usunięty.")
    else:
        print("Nie znaleziono pokazu.")


def duplicate_show(db): print("Powielanie pokazu...")


def show_shows(db): print("Wyświetlenie shows")


def log_as_event_creator(db):
    email = input("podaj email: ")
    password = input("podaj hasło: ")
    person = EventCreator.login_person(db, email, password)
    if person:
        event_creator_menu(person)
    else:
        print('nieprawidłowy login lub hasło')
        main_menu(db)


def log_as_participant(db):
    email = input("podaj email: ")
    password = input("podaj hasło: ")
    person = Participant.login_person(db, email, password)
    if person:
        participant_menu(person)
    else:
        print('nieprawidłowy login lub hasło')
        main_menu(db)


# Funkcja głównego menu dla EventCreatora
def main_menu(db):
    options = {
        '1': ("zaloguj jako Organizator", lambda: log_as_event_creator(db),),
        '2': ("zaloguj jako Uczestnik", lambda: log_as_participant(db),),
        '0': ("Koniec pracy", exit)
    }

    menu("Główne", options)


def event_creator_menu(event_creator):
    options = {
        '1': ("Stwórz wydarzenie", lambda: create_event(event_creator),),
        '2': ("Edytuj wydarzenie", lambda: edit_event(event_creator),),
        '3': ("Usuń wydarzenie", lambda: delete_event(event_creator),),
        '4': ("Powiel wydarzenie", lambda: duplicate_event(event_creator),),
        '5': ("Wyświetl wydarzenia", lambda: show_events(event_creator),),
        '0': ("Powrót do głównego menu (wyloguj)", lambda: main_menu(event_creator.db),)
    }
    menu(f"Organizatora ({event_creator.person_id})", options)


# Funkcja głównego menu dla Participant
def participant_menu(participant):
    options = {
        '1': ("Wyświetl listę wydarzeń", show_events(participant),),
        '2': ("Kup bilet", buy_ticket(participant),),
        '3': ("Zwróć bilet", return_ticket(participant),),
        '4': ("Pokaż moje bilety", show_my_tickets(participant),),
        '0': ("Powrót do głównego menu (wyloguj)", lambda: main_menu(participant.db),)
    }
    menu("Participant ({person.person_id})", options)



# Funkcja głównego menu dla Show
def show_menu(db):
    options = {
        '1': ("Stwórz pokaz", create_show(db),),
        '2': ("Edytuj pokaz", edit_show(db),),
        '3': ("Skasuj pokaz", delete_show(db),),
        '4': ("Powiel pokaz", duplicate_show(db),),
        '5': ("Wyświetl pokazy", show_shows(db),),
        '0': ("Powrót do głównego menu", main_menu(db),)
    }
    menu("Show", options)
