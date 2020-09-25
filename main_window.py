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
    def __init__(self, database):
        self.db = database
        self.window = Tk()
        self.window.title('Моя Библиотека | MyLib')
        self.greetings_text = Label(self.window, text='Добро пожаловать в библиотеку MyLib',
                                    font=('TimesNewRoman', 16), pady='20', padx='20')

        self.button_searching = Button(self.window , text='Найти / Удалить / Изменить книги',
                                       background="#555",
                                       foreground="#ccc", padx="135",
                                       font=('TimesNewRoman', 13), command=self.open_adding_window())

        self.button_adding = Button(self.window , text='Добавить книги',
                                    background="#555", foreground="#ccc",
                                    padx="100", font=('TimesNewRoman', 13),
                                    command=self.open_searching_window())

        self.greetings_text.pack(fill='both')
        self.button_searching.pack(fill='both', side='bottom')
        self.button_adding.pack(fill='both', side='bottom')

        self.window.mainloop()

    def open_adding_window(self):
        self.window.withdraw()
        AddBook(self.db, self)

    def open_searching_window(self):
        pass


class AddBook:
    """
    Функция-окно добавления книг
    :return:
    """
    def __init__(self, database, parent=None):
        self.parent = parent
        self.db = database
        self.window = Tk()
        self.top_frame = Frame(self.window)
        self.bottom_frame = Frame(self.window)
        self.left_frame = Frame(self.window)
        self.right_frame = Frame(self.window)
        self.book_add_text = Label(self.top_frame, text='Введите данные о добавляемой книге',
                                      font=('TimesNewRoman', 15), pady='20', padx='10')
        self.book_year_text = Label(self.left_frame, text='Год издания:',
                                       font=('TimesNewRoman', 13))
        self.book_year_field = Entry(self.right_frame, width=40)
        self.book_author_text = Label(self.left_frame, text='Автор:',
                                         font=('TimesNewRoman', 13))
        self.book_author_field = Entry(self.right_frame, width=40)
        self.book_name_text = Label(self.left_frame, text='Название:',
                                       font=('TimesNewRoman', 13))
        self.book_name_field = Entry(self.right_frame, width=40)
        self.button_back = tkinter.Button(self.bottom_frame, text='Назад',
                                     background="#555", foreground="#ccc",
                                     padx="70", font=('TimesNewRoman', 13), command=self.backing())
        self.button_add = tkinter.Button(self.bottom_frame, text='Добавить',
                                    background="#555", foreground="#ccc",
                                    padx="70", font=('TimesNewRoman', 13), command=self.adding())
        self.button_add_file = tkinter.Button(self.bottom_frame, text='Добавить несколько '
                                                               'из файла csv', background="#555",
                                         foreground="#ccc", padx="70",
                                         font=('TimesNewRoman', 13), command=self.add_file())




        self.window.title('Добавление книги | MyLib')
        self.top_frame.pack(side='top')
        self.bottom_frame.pack(side='bottom')
        self.left_frame.pack(side='left')
        self.right_frame.pack(side='right', fill='x', expand=True)
        self.book_add_text.pack(fill='both')
        self.book_year_text.pack()
        self.book_year_field.pack(fill='x', expand=True)
        self.book_year_field.focus()
        self.book_author_text.pack()
        self.book_author_field.pack(fill='x', expand=True)
        self.book_name_text.pack()
        self.book_name_field.pack(fill='x', expand=True)
        self.button_back.pack(side='left')
        self.button_add.pack(side='left')
        self.button_add_file.pack(side='bottom')
        self.window.protocol("WM_DELETE_WINDOW", self.closing())

        self.window.mainloop()

    def backing(self):
        """
        функция для кнопки "Назад(домой)"
        :return:
        """
        self.window.destroy()
        self.parent.deiconify()###########

    def adding(self) -> NoReturn:
        """
        добавление одной книги со внесенными параметрами
        :return:
        """
        res = (self.book_year_field.get(), self.book_author_field.get(), self.book_name_field.get())
        if res[0] and not res[0].isdigit():
            self.book_year_text.configure(text='Год издания (необходимо указать '
                                          'год в числовом формате):', fg='red')
            res = (None, None, None)
        if not res[2]:
            self.book_name_text.configure(text='Название (это поле обязательно '
                                          'для заполнения):', fg='red')
            res = (None, None, None)
        if res != (None, None, None):
            if res not in sql.execute("SELECT * FROM books"):
                messagebox.showinfo('MyLib', f'Книга \'{res[2]}\' успешно '
                f'добавлена в библиотеку')
                sql.execute("INSERT INTO books VALUES (?, ?, ?)", res)
                db.commit()
                self.window.destroy()
                AddBook(self.db, self.parent)
            else:
                messagebox.showinfo('MyLib', f'Книга \'{res[2]}\' '
                f'уже имеется в библиотеке')

    def add_file(self) -> NoReturn:
        """
        Добавление коллекции книг из файла csv
        :return:
        """
        file_name = filedialog.askopenfilename(filetypes=[('CSV', '*.csv')])
        try:
            with open(file_name, "r") as file:
                reader = csv.reader(file)
                incorrect_year = ''
                incorrect_name = ''
                book_copy = ''
                new_books = set()
                for row in reader:
                    book = tuple([row[0].strip(), row[1].strip(), row[2].strip()])
                    if book[0] and not book[0].isdigit():
                        incorrect_year = 'Обнаружены позиции с некорректным годом издания\n'
                        continue
                    if not book[2]:
                        incorrect_name = 'Обнаружены позиции без названия\n'
                        continue
                    if book in sql.execute("SELECT * FROM books"):
                        book_copy = 'Обнаружены позиции уже имеющиеся в библиотеке\n'
                        continue
                    new_books.add(book)
                if incorrect_name != '' or incorrect_year != '' or book_copy != '':
                    add_confirm = messagebox.askyesno('MyLib', f'В файле обнаружены '
                    f'следующие ошибки:\n\n'
                    f'{incorrect_year}'
                    f'{incorrect_name}'
                    f'{book_copy}\n'
                    f'Игнорировать эти '
                    f'позиции и продолжить загрузку? ')
                    if add_confirm:
                        sql.executemany("INSERT INTO books VALUES (?, ?, ?)", new_books)
                        db.commit()
                        messagebox.showinfo('MyLib', 'Книги успешно добавлены в библиотеку')
                else:
                    sql.executemany("INSERT INTO books VALUES (?, ?, ?)", new_books)
                    db.commit()
                    messagebox.showinfo('MyLib', 'Книги успешно добавлены в библиотеку')
        except FileNotFoundError:
            pass
        except TypeError:
            pass

    def closing(self) -> NoReturn:
        """
        Завершение работы программы
        :return:
        """
        if messagebox.askokcancel("MyLib", "Завершить работу в MyLib?"):
            self.window.destroy()
            self.parent.destroy()
            db.close()



=========================================================================================================


main_window = MainMenu()
db.close()
