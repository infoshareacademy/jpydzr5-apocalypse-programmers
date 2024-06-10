TICKET_PRICE = 10
SERVICE_CHARGE = 2

tickets_remaining = 100


def calculate_price(ticket_amount):
    return (ticket_amount * TICKET_PRICE) + SERVICE_CHARGE


while tickets_remaining >= 1:
    print(f'There are {tickets_remaining} tickets remaining')

    # Capture the user's name and assign it to a new variable
    name = input('What is your name?: ')

    # Ask how many tickets they would like and calculate the price
    ticket_amount = input(f'{name}, How many tickets would you like?: ')
    # Expect a ValueError to happen and handle it appropriately
    try:
        ticket_amount = int(ticket_amount)
        # Raise a ValueError if the request is more tickets than there are available
        if ticket_amount > tickets_remaining:
            raise ValueError(f'Sorry, there are only {tickets_remaining} tickets remaining.')
    except ValueError as err:
        print(f'Sorry, invalid input {err}')
    else:
        price = calculate_price(ticket_amount)
        print(f'Your total is ${price} for {ticket_amount} tickets')

        # Prompt the user if they want to proceed Y/N
        proceed = input('Would you like to proceed with your purchase? yes/no: ')
        if 'y' in proceed.lower():

            # TODO: Gather credit card information and process it

            print('Sold!')
            tickets_remaining -= ticket_amount
        else:
            print(f'Thank you {name}, hope to see you again soon.')

# Notify the user when the tickets are sold out
print('Sorry, the tickets are sold out.')