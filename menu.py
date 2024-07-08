# Funkcja głównego menu dla EventCreatora
def event_creator_menu():
    options = {
        '1': ("Stwórz wydarzenie", create_event),
        '2': ("Edytuj wydarzenie", edit_event),
        '3': ("Usuń wydarzenie", delete_event),
        '4': ("Powiel wydarzenie", duplicate_event),
        '0': ("Wyjdź", exit)
    }
    menu("EventCreatora", options)

# Funkcja głównego menu dla Participant
def participant_menu():
    options = {
        '1': ("Wyświetl listę wydarzeń", show_events),
        '2': ("Kup bilet", buy_ticket),
        '3': ("Zwróć bilet", return_ticket),
        '4': ("Pokaż moje bilety", show_my_tickets),
        '0': ("Wyjdź", exit)
    }
    menu("Participant", options)

# Funkcja głównego menu dla Show
def show_menu():
    options = {
        '1': ("Stwórz pokaz", create_show),
        '2': ("Edytuj pokaz", edit_show),
        '3': ("Skasuj pokaz", delete_show),
        '4': ("Powiel pokaz", duplicate_show),
        '0': ("Wyjdź", exit)
    }
    menu("Show", options)

# Ogólna funkcja menu dla powtarzających się opcji
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

# Przykładowe funkcje dla opcji menu
def create_event(): print("Tworzenie wydarzenia...")
def edit_event(): print("Edycja wydarzenia...")
def delete_event(): print("Usuwanie wydarzenia...")
def duplicate_event(): print("Powielanie wydarzenia...")
def show_events(): print("Wyświetlanie listy wydarzeń...")
def buy_ticket(): print("Kupowanie biletu...")
def return_ticket(): print("Zwracanie biletu...")
def show_my_tickets(): print("Wyświetlanie moich biletów...")
def create_show(): print("Tworzenie pokazu...")
def edit_show(): print("Edycja pokazu...")
def delete_show(): print("Usuwanie pokazu...")
def duplicate_show(): print("Powielanie pokazu...")

# Przykład uruchomienia menu EventCreatora
event_creator_menu()
