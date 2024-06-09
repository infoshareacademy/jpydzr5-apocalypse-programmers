from tkinter import *
from tkinter import messagebox
import random
import string

def show_message(title, message):
    """Pokazuje wiadomosci oraz bledy"""
    messagebox.showerror(title, message)


def get_random_string(self):
    """generuje losowy oraz unikatowy id

    na razie nie wykorzystywane
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(8))