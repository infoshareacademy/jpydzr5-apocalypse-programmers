from typing import List
from tkinter import *
from tkinter import messagebox
import random
import string
import json

def save_objects_to_json(data: List, filename: str) -> bool:
    """ zapisuje listę do pliku csv"""
    data_as_dicts = [obj.to_dict() for obj in data]
    print(data_as_dicts)
    with open(filename, "w") as f:
        json.dump(data_as_dicts, f)

        
def show_message(title, message):
    """Pokazuje wiadomosci oraz bledy"""
    messagebox.showerror(title, message)


def get_random_string(self):
    """generuje losowy oraz unikatowy id"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(8))