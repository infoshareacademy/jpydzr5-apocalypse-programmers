from Menu_list import *

get_list = Menu_list("get_list")
option = ''
while option != '6':
    option = input("""Select an option:
1)event;
2)participant;
3)show;
4)ticket;
5)eventcreator;
: """)


    match option:
        case "event":
            def print_menu_event():
                print("------------------------------")
                print("Select an option")
                print("1. Create a Event")
                print("2. Read a Event")
                print("3. Update a Event")
                print("4. Delete a Event")
                print("------------------------------")


            while True:
                print_menu_event()
                option = input("Make a choice >> ")

                if option == "1":
                    new_event = input("Enter a Event name: ")
                    get_list.event_list.append(new_event)
                elif option == "2":
                    get_list.display_all()
                elif option == "3":
                    print("Update a Event")
                elif option == "4":
                    print("Delete a Event")
                else:
                    print("Invalid option, please try again")


        case "participant":
            def print_menu_participant():
                print("------------------------------")
                print("Select an option")
                print("1. Create a Participant")
                print("2. Read a Participant")
                print("3. Update a Participant")
                print("4. Delete a Participant")
                print("------------------------------")


            while True:
                print_menu_participant()
                option = input("Make a choice >> ")

                if option == "1":
                    new_participant = input("Enter a Participant name: ")
                    get_list.participant_list.append(new_participant)
                elif option == "2":
                    get_list.display_all()
                elif option == "3":
                    print("Update a Participant")
                elif option == "4":
                    print("Delete a Participant")
                else:
                    print("Invalid option, please try again")



        case "show":
            def print_menu_show():
                print("------------------------------")
                print("Select an option")
                print("1. Create a Show")
                print("2. Read a Show")
                print("3. Update a Show")
                print("4. Delete a Show")
                print("------------------------------")


            while True:
                print_menu_show()
                option = input("Make a choice >> ")

                if option == "1":
                    new_show = input("Enter a Show name: ")
                    get_list.show_list.append(new_show)
                elif option == "2":
                    get_list.display_all()
                elif option == "3":
                    print("Update a Show")
                elif option == "4":
                    print("Delete a Show")
                else:
                    print("Invalid option, please try again")



        case "ticket":
            def print_menu_ticket():
                print("------------------------------")
                print("Select an option")
                print("1. Create a Ticket")
                print("2. Read a Ticket")
                print("3. Update a Ticket")
                print("4. Delete a Ticket")
                print("------------------------------")


            while True:
                print_menu_ticket()
                option = input("Make a choice >> ")

                if option == "1":
                    new_ticket = input("Enter a Ticket name: ")
                    get_list.ticket_list.append(new_ticket)
                elif option == "2":
                    get_list.display_all()
                elif option == "3":
                    print("Update a Ticket")
                elif option == "4":
                    print("Delete a Ticket")
                else:
                    print("Invalid option, please try again")
                    break



        case "eventCreator":
            def print_menu_eventcreator():
                print("------------------------------")
                print("Select an option")
                print("1. Create a EventCreator")
                print("2. Read a EventCreator")
                print("3. Update a EventCreator")
                print("4. Delete a EventCreator")
                print("------------------------------")


            while True:
                print_menu_eventcreator()
                option = input("Make a choice >> ")

                if option == "1":
                    new_eventcreator = input("Enter a EventCreator name: ")
                    get_list.event_list.append(new_eventcreator)
                elif option == "2":
                    get_list.display_all()
                elif option == "3":
                    print("Update a EventCreator")
                elif option == "4":
                    print("Delete a EventCreator")
                else:
                    print("Invalid option, please try again")
                break

        case _:
            print("again")

