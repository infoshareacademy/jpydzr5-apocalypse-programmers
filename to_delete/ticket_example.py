class Ticket:
    def __init__(self, event_name, price, tickets_remaining):
        self.event_name = event_name
        self.price = price
        self.tickets_remaining = tickets_remaining


event1 = Ticket('Lady Gaga', 25, 200)
event2 = Ticket('Just Dance', 30, 100)
event3 = Ticket('Our Coming Tomek!', 100, 2)

option = input('What do you want to see:'
               'A)Lady Gaga;'
               'B)Just Dance;'
               'C)Our Coming Tomek;')

match option:
    case 'A':
        while event1.tickets_remaining >= 1:
            print(f'There are {event1.tickets_remaining} tickets remaining')

            # Capture the user's name and assign it to a new variable
            name = input('What is your name?: ')

            # Ask how many tickets they would like and calculate the price
            ticket_amount = input(f'{name}, How many tickets would you like?: ')
            # Expect a ValueError to happen and handle it appropriately
            try:
                ticket_amount = int(ticket_amount)
                # Raise a ValueError if the request is more tickets than there are available
                if ticket_amount > event1.tickets_remaining:
                    raise ValueError(f'Sorry, there are only {event1.tickets_remaining} tickets remaining.')
            except ValueError as err:
                print(f'Sorry, invalid input {err}')
            else:
                price = ticket_amount * event1.price
                print(f'Your total is ${price} for {ticket_amount} tickets')

                # Prompt the user if they want to proceed Y/N
                proceed = input('Would you like to proceed with your purchase? yes/no: ')
                if 'y' in proceed.lower():

                    # TODO: Gather credit card information and process it

                    print('Sold!')
                    event1.tickets_remaining -= ticket_amount
                else:
                    print(f'Thank you {name}, hope to see you again soon.')

        # Notify the user when the tickets are sold out
        print('Sorry, the tickets are sold out.')

    case 'B':
        while event2.tickets_remaining >= 1:
            print(f'There are {event2.tickets_remaining} tickets remaining')

            # Capture the user's name and assign it to a new variable
            name = input('What is your name?: ')

            # Ask how many tickets they would like and calculate the price
            ticket_amount = input(f'{name}, How many tickets would you like?: ')
            # Expect a ValueError to happen and handle it appropriately
            try:
                ticket_amount = int(ticket_amount)
                # Raise a ValueError if the request is more tickets than there are available
                if ticket_amount > event2.tickets_remaining:
                    raise ValueError(f'Sorry, there are only {event2.tickets_remaining} tickets remaining.')
            except ValueError as err:
                print(f'Sorry, invalid input {err}')
            else:
                price = ticket_amount * event2.price
                print(f'Your total is ${price} for {ticket_amount} tickets')

                # Prompt the user if they want to proceed Y/N
                proceed = input('Would you like to proceed with your purchase? yes/no: ')
                if 'y' in proceed.lower():

                    # TODO: Gather credit card information and process it

                    print('Sold!')
                    event2.tickets_remaining -= ticket_amount
                else:
                    print(f'Thank you {name}, hope to see you again soon.')


        # Notify the user when the tickets are sold out
        print('Sorry, the tickets are sold out.')

    case 'C':
        while event3.tickets_remaining >= 1:
            print(f'There are {event3.tickets_remaining} tickets remaining')

            # Capture the user's name and assign it to a new variable
            name = input('What is your name?: ')

            # Ask how many tickets they would like and calculate the price
            ticket_amount = input(f'{name}, How many tickets would you like?: ')
            # Expect a ValueError to happen and handle it appropriately
            try:
                ticket_amount = int(ticket_amount)
                # Raise a ValueError if the request is more tickets than there are available
                if ticket_amount > event3.tickets_remaining:
                    raise ValueError(f'Sorry, there are only {event3.tickets_remaining} tickets remaining.')
            except ValueError as err:
                print(f'Sorry, invalid input {err}')
            else:
                price = ticket_amount * event3.price
                print(f'Your total is ${price} for {ticket_amount} tickets')

                # Prompt the user if they want to proceed Y/N
                proceed = input('Would you like to proceed with your purchase? yes/no: ')
                if 'y' in proceed.lower():

                    # TODO: Gather credit card information and process it

                    print('Sold!')
                    event3.tickets_remaining -= ticket_amount
                else:
                    print(f'Thank you {name}, hope to see you again soon.')

        # Notify the user when the tickets are sold out
        print('Sorry, the tickets are sold out.')