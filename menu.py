import os
import pendulum
import platform
import subprocess
from decimal import Decimal
from classes import EventCreator, Participant, Event, Show, Ticket


def clear_screen():
    current_os = platform.system()

    if current_os == "Windows":
        # Sprawdzenie czy jest PowerShell, jeśli nie, użyj 'cls'
        if subprocess.run(["powershell", "-Command", "Clear-Host"]).returncode != 0:
            os.system('cls')
    else:
        os.system('clear')


# Ogólna funkcja menu dla powtarzających się opcji
def menu(title, options):
    while True:
        clear_screen()
        menu_title = f" Menu {title.strip()} "
        print(f"{menu_title:-^80}")
        for key, (description, _) in options.items():
            if key == '0':
                print('')
            print(f"{key}. {description}")
        choice = input("\nWybierz opcję: ")
        if choice in options:
            options[choice][1]()
        else:
            print("Niepoprawny wybór, spróbuj ponownie.")


def menu_header(title, break_line=True):
    title = f" {title.strip()} "
    return f"{'\n' if break_line else ''}{title:=^80}"


def create_event(event_creator):
    print(menu_header('Tworzenie wydarzenia'))
    name = input('Podaj nazwę wydarzenia: ')
    event_type = input('Podaj typ wydarzenia (np. Koncert, Standup): ')
    event_creator.create_event(name, event_type)
    print("Wydarzenie utworzone.")
    return


def rename_event(event_creator):
    print(menu_header('Edycja wydarzenia'))
    try:
        event_id = int(input("Podaj ID wydarzenia do edycji: "))
    except ValueError:
        print("nieprawidłowa wartość")
        return

    event = Event.get_by_id(event_creator.db, event_id)
    if event:
        new_name = input(f"Podaj nową nazwę wydarzenia [{event.name}]: ")
        if new_name:
            event_creator.name = new_name
        print("Wydarzenie zaktualizowane.")
    else:
        print("Nie znaleziono wydarzenia.")
    return


def delete_event(event_creator):
    print(menu_header('Usuwanie wydarzenia'))
    try:
        event_id = int(input("Podaj ID wydarzenia do usunięcia: "))
    except ValueError:
        print("nieprawidłowa wartość")
        return

    event = Event.get_by_id(event_creator.db, event_id)
    if event:
        event_creator.delete_event(event)
        print("Wydarzenie usunięte.")
    else:
        print("Nie znaleziono wydarzenia.")
    return


def duplicate_event(event_creator):
    print(menu_header('Powielanie wydarzenia'))
    try:
        event_id = int(input("Podaj ID wydarzenia do powielenia: "))
    except ValueError:
        print("nieprawidłowa wartość")
        return

    event = Event.get_by_id(event_creator.db, event_id)
    if event:
        event_creator.create_event(f"{event.name}_kopia", event.event_type)
        print("Wydarzenie powielone.")
    else:
        print("Nie znaleziono wydarzenia.")
    return


def show_events(event_creator, press_enter=True):
    print(menu_header('Lista wydarzeń'))
    events = event_creator.get_my_events()
    for event in events:
        print(f"{event.event_id}. {event.name} ({event.event_type})")
    if press_enter:
        input('Naciśnij ENTER by kontynuować')
    return


def go_to_event_menu(event_creator):
    print(menu_header('Edycja wydarzenia'))
    try:
        event_id = int(input("Podaj ID wydarzenia do edycji: "))
    except ValueError:
        print("nieprawidłowa wartość")
        return

    event = Event.get_by_id(event_creator.db, event_id)
    if event:
        event_menu(event)
    else:
        print("Nie znaleziono wydarzenia.")
    return


def buy_ticket(db, participant):
    print(menu_header('Kupowanie biletu'))
    try:
        show_id = int(input("Podaj ID pokazu: "))
    except ValueError:
        print("nieprawidłowa wartość")
        return

    show = Show.get_by_id(participant.db, show_id)
    if show:
        ticket = participant.buy_ticket(show)
        print("Bilet kupiony.")
    else:
        print("Nie znaleziono pokazu.")
    return


def return_ticket(db, participant):
    print(menu_header('Zwrot biletu'))
    try:
        ticket_id = int(input("Podaj ID biletu do zwrotu: "))
    except ValueError:
        print("nieprawidłowa wartość")
        return

    ticket = Ticket.get_by_id(participant.db, ticket_id)
    if ticket:
        ticket.cancel_ticket()
        print("Bilet zwrócony.")
    else:
        print("Nie znaleziono biletu.")
    return


def show_my_tickets(db):
    print(menu_header('Lista moich biletów'))
    print("TODO: Wyświetlanie moich biletów")
    return


def create_show(event):
    print(menu_header(f"{event.name} ({event.event_type})"))
    print(menu_header('Tworzenie pokazu', False))
    name = input("Podaj nazwę pokazu: ")
    start_time = pendulum.parse(input("Podaj czas rozpoczęcia (YYYY-MM-DD HH:MM): "))
    end_time = pendulum.parse(input("Podaj czas zakończenia (YYYY-MM-DD HH:MM): "))
    price = Decimal(input("Podaj cenę biletu: "))
    event.create_show(name, start_time, end_time, price)
    print("Pokaz utworzony.")
    return


def rename_show(event):
    print(menu_header('Edycja pokazu'))
    show_shows(event, False)
    try:
        show_id = int(input("Podaj ID pokazu do edycji: "))
    except ValueError:
        print("nieprawidłowa wartość")
        return

    show = Show.get_by_id(event.db, show_id)
    if show:
        new_name = input(f"Podaj nową nazwę pokazu [{show.name}]: ")
        if new_name:
            show.name = new_name
        print("Nazwa pokazu zmieniona.")
    else:
        print("Nie znaleziono pokazu.")
    return


def change_show_price(event):
    print(menu_header('Zmiana ceny pokazu'))
    show_shows(event, False)
    try:
        show_id = int(input("Podaj ID pokazu do edycji: "))
    except ValueError:
        print("nieprawidłowa wartość")
        return

    show = Show.get_by_id(event.db, show_id)
    if show:
        new_price = Decimal(input(f"Podaj nową cenę pokazu [{show.price}]: "))
        if new_price:
            show.price = new_price
        print("Cena zmieniona.")
    else:
        print("Nie znaleziono pokazu.")
    return


def delete_show(event):
    print(menu_header('Usuwanie pokazu'))
    show_shows(event, False)
    try:
        show_id = int(input("Podaj ID pokazu do usunięcia: "))
    except ValueError:
        print("nieprawidłowa wartość")
        return

    show = Show.get_by_id(event.db, show_id)
    if show:
        event.delete_show(show)
        print("Pokaz usunięty.")
    else:
        print("Nie znaleziono pokazu.")
    return


def duplicate_show(event):
    print(menu_header('Powielanie pokazu'))
    show_shows(event, False)
    try:
        show_id = int(input("Podaj ID pokazu do powielenia: "))
    except ValueError:
        print("nieprawidłowa wartość")
        return

    show = Show.get_by_id(event.db, show_id)
    if show:
        event.create_show(f"{show.name}_kopia", show.start_time, show.end_time, show.price)
        print("Wydarzenie powielone.")
    else:
        print("Nie znaleziono pokazu.")
    return


def show_shows(event, press_enter=True):
    print(menu_header(f"{event.name} ({event.event_type})"))
    print(menu_header('Lista pokazów', False))
    shows = event.get_my_shows()
    for show in shows:
        print(f"{show.list_item()}")
    if press_enter:
        input('Naciśnij ENTER by kontynuować')
    return


def return_to_event_creator_menu(event):
    event_creator = EventCreator.get_by_id(event.db, event.creator_id)
    event_creator_menu(event_creator)
    return


def log_as_event_creator(db):
    email = input("podaj email: ")
    password = input("podaj hasło: ")
    person = EventCreator.login_person(db, email, password)
    if person:
        event_creator_menu(person)
    else:
        print('nieprawidłowy login lub hasło')
        main_menu(db)
    return


def log_as_participant(db):
    email = input("podaj email: ")
    password = input("podaj hasło: ")
    person = Participant.login_person(db, email, password)
    if person:
        participant_menu(person)
    else:
        print('nieprawidłowy login lub hasło')
        main_menu(db)
    return


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
        '2': ("Usuń wydarzenie", lambda: delete_event(event_creator),),
        '3': ("Powiel wydarzenie", lambda: duplicate_event(event_creator),),
        '4': ("Wyświetl wydarzenia", lambda: show_events(event_creator),),
        '5': ("Zmień nazwę wydarzenia", lambda: rename_event(event_creator),),
        '9': ("Menu pokazów", lambda: go_to_event_menu(event_creator),),
        '0': ("Powrót do głównego menu (wyloguj)", lambda: main_menu(event_creator.db),)
    }
    menu(f"Organizatora ({event_creator.person_id})", options)


def event_menu(event):
    options = {
        '1': ("Dodaj pokaz", lambda: create_show(event),),
        '2': ("Usuń pokaz", lambda: delete_show(event),),
        '3': ("Powiel pokaz", lambda: duplicate_show(event),),
        '4': ("Wyświetl pokazy", lambda: show_shows(event),),
        '5': ("Zmień nazwę pokazu", lambda: rename_show(event),),
        '6': ("Zmień cenę pokazu", lambda: change_show_price(event),),

        '0': ("Powrót do Menu Organizatora", lambda: return_to_event_creator_menu(event),)
    }
    menu(f"Wydarzenia ({event.name})", options)


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
