class Menu_list:
    def __init__(self, list_name):
        self.list_name = list_name
        self.event_list = []
        self.participant_list = []
        self.show_list = []
        self.ticket_list = []
        self.eventcreator_list = []

    def display_all(self):
        for i in (self.event_list, self.participant_list, self.show_list, self.ticket_list, self.ticket_list,
                  self.eventcreator_list
                  ):
            print(i)