class Ticket:
    def __init__(self, event_name, price, tickets_remaining):
        self.event_name = event_name
        self.price = price
        self.tickets_remaining = tickets_remaining


event1 = Ticket('Lady Gaga', 25, 200)
event2 = Ticket('Just Dance', 30, 100)
event3 = Ticket('Our Coming Tomek!', 100, 2)

x = event1.tickets_remaining

while x >= 1:

    print(f'There are {x} tickets remaining')

    # Capture the user's name and assign it to a new variable
    name = input('What is your name?: ')

    # Ask how many tickets they would like and calculate the price
    ticket_amount = input(f'{name}, How many tickets would you like?: ')
    # Expect a ValueError to happen and handle it appropriately
    try:
        ticket_amount = int(ticket_amount)
        # Raise a ValueError if the request is more tickets than there are available

        if ticket_amount > x:
            raise ValueError(f'Sorry, there are only {x} tickets remaining.')
    except ValueError as err:
        print(f'Sorry, invalid input {err}')
    else:
        print(f'Your total is ${event1.price} for {ticket_amount} tickets')

        # Prompt the user if they want to proceed Y/N
        proceed = input('Would you like to proceed with your purchase? yes/no: ')
        if 'y' in proceed.lower():

            # TODO: Gather credit card information and process it

            print('Sold!')

            x -= ticket_amount
        else:
            print(f'Thank you {name}, hope to see you again soon.')

# Notify the user when the tickets are sold out
print('Sorry, the tickets are sold out.')