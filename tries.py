import csv
from typing import NoReturn

import sqlite3
import tkinter
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import *

db = sqlite3.connect('biblioteka.db')
sql = db.cursor()
sql.execute('''CREATE TABLE IF NOT EXISTS books (
    year TEXT,
    author TEXT,
    name TEXT
    )''')
db.commit()


class MainMenu:
    def __init__(self, title):
        self.window = Tk()
        self.greetings_text = Label(self.window, text='Добро пожаловать в библиотеку MyLib',
                                    font=('TimesNewRoman', 16), pady='20', padx='20')
        self.button_searching = Button(self.window , text='Найти / Удалить / Изменить книги',
                                       background="#555",
                                       foreground="#ccc", padx="135",
                                       font=('TimesNewRoman', 13), command=None)
        self.button_adding = Button(self.window , text='Добавить книги',
                                    background="#555", foreground="#ccc",
                                    padx="100", font=('TimesNewRoman', 13),
                                    command=None)

        self.greetings_text.pack(fill='both')
        self.button_searching.pack(fill='both', side='bottom')
        self.button_adding.pack(fill='both', side='bottom')
        self.window.title(title)
        self.window.mainloop()


main_window = MainMenu('Моя Библиотека | MyLib')
db.close()
