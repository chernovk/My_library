import csv
import json
from abc import ABC

import sqlite3
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import *

from book import Book

db = sqlite3.connect('lib.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
    year TEXT,
    author TEXT,
    name TEXT
    )''')
db.commit()


class MainMenu:
    def __init__(self):
        self.window = Tk()
        self.window.title('Моя Библиотека | MyLib')
        self.greetings_text = Label(self.window, text='Добро пожаловать в библиотеку MyLib',
                                    font=('TimesNewRoman', 16), pady='20', padx='20')

        self.button_searching = Button(self.window, text='Найти / Удалить / Изменить книги',
                                       background="#555",
                                       foreground="#ccc", padx="135",
                                       font=('TimesNewRoman', 13), command=self.open_searching_window)

        self.button_adding = Button(self.window, text='Добавить книги',
                                    background="#555", foreground="#ccc",
                                    padx="100", font=('TimesNewRoman', 13),
                                    command=self.open_adding_window)

        self.greetings_text.pack(fill='both')
        self.button_searching.pack(fill='both', side='bottom')
        self.button_adding.pack(fill='both', side='bottom')

        self.window.mainloop()

    def open_adding_window(self):
        self.window.withdraw()
        AddBook(self)

    def open_searching_window(self):
        self.window.withdraw()
        SearchBook(self)


class BookForm(ABC):
    """
    Функция-окно добавления книг
    :return:
    """
    def __init__(self, parent=None, chosen_book=None):
        self.book_info_to_update = chosen_book
        self.parent = parent
        self.window = Tk()
        self.top_frame = Frame(self.window)
        self.bottom_frame = Frame(self.window)
        self.left_frame = Frame(self.window)
        self.right_frame = Frame(self.window)

        self.book_year_text = Label(self.left_frame, text='Год издания:',
                                    font=('TimesNewRoman', 13))
        self.book_year_field = Entry(self.right_frame, width=40)
        self.book_author_text = Label(self.left_frame, text='Автор:',
                                      font=('TimesNewRoman', 13))
        self.book_author_field = Entry(self.right_frame, width=40)
        self.book_name_text = Label(self.left_frame, text='Название:',
                                    font=('TimesNewRoman', 13))
        self.book_name_field = Entry(self.right_frame, width=40)
        self.button_back = Button(self.bottom_frame, text='Назад',
                                  background="#555", foreground="#ccc",
                                  padx="70", font=('TimesNewRoman', 13), command=self.backing)

        self.window.title('Добавление книги | MyLib')
        self.top_frame.pack(side='top')
        self.bottom_frame.pack(side='bottom')
        self.left_frame.pack(side='left')
        self.right_frame.pack(side='right', fill='x', expand=True)
        self.header.pack(fill='both')
        self.book_year_text.pack()
        self.book_year_field.pack(fill='x', expand=True)
        self.book_year_field.focus()
        self.book_author_text.pack()
        self.book_author_field.pack(fill='x', expand=True)
        self.book_name_text.pack()
        self.book_name_field.pack(fill='x', expand=True)
        self.button_back.pack(side='left')
        self.action_button.pack(side='left')
        self.window.protocol("WM_DELETE_WINDOW", self.closing)
        if self.book_info_to_update:
            self.book_year_field.insert(0, self.book_info_to_update[0])
            self.book_author_field.insert(0, self.book_info_to_update[1])
            self.book_name_field.insert(0, self.book_info_to_update[2])
        if self.extra_button:
            self.extra_button.pack(side='bottom')

        self.window.mainloop()

    @property
    def header(self):
        return Label(self.top_frame, text='???',
                     font=('TimesNewRoman', 15), pady='20', padx='10')

    @property
    def action_button(self):
        return Button(self.bottom_frame, text='???', background="#555", foreground="#ccc",
                      padx="70", font=('TimesNewRoman', 13), command=None)

    @property
    def extra_button(self):
        return None

    def backing(self):
        """
        функция для кнопки "Назад(домой)"
        :return:
        """
        self.window.destroy()
        self.parent.window.deiconify()

    def closing(self):
        """
        Завершение работы программы
        :return:
        """
        if messagebox.askokcancel("MyLib", "Завершить работу в MyLib?"):
            self.window.destroy()
            self.parent.window.destroy()
            db.close()


class AddBook(BookForm):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    @property
    def extra_button(self):
        return Button(self.bottom_frame, text='Добавить несколько из csv/json', background="#555",
                      foreground="#ccc", padx="70",
                      font=('TimesNewRoman', 13), command=self.add_file)

    @property
    def header(self):
        return Label(self.top_frame, text='Введите данные о добавляемой книге',
                     font=('TimesNewRoman', 15), pady='20', padx='10')

    @property
    def action_button(self):
        return Button(self.bottom_frame, text='Добавить', background="#555", foreground="#ccc",
                      padx="70", font=('TimesNewRoman', 13), command=self.adding)

    @staticmethod
    def add_file():
        """
        Добавление коллекции книг из файла csv / json
        :return:
        """
        file_name = filedialog.askopenfilename(filetypes=[('CSV', '*.csv'), ('JSON', '*.json')])
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                if file_name.endswith('.csv'):
                    list_of_books = csv.reader(file)
                elif file_name.endswith('.json'):
                    list_of_books = json.load(file)

                incorrect_year = ''
                incorrect_name = ''
                book_copy = ''
                new_books = []
                for row in list_of_books:
                    if file_name.endswith('.csv'):
                        book = tuple([row[0].strip(), row[1].strip(), row[2].strip()])
                    elif file_name.endswith('.json'):
                        book = tuple([row["Год выпуска"].strip(), row["Автор"].strip(),
                                      row["Название"].strip()])
                    if book[0] and not book[0].isdigit():
                        incorrect_year = 'Обнаружены позиции с некорректным годом издания\n'
                        continue
                    if not book[2]:
                        incorrect_name = 'Обнаружены позиции без названия\n'
                        continue
                    if book in cursor.execute("SELECT * FROM books"):
                        book_copy = 'Обнаружены позиции уже имеющиеся в библиотеке\n'
                        continue
                    new_books.append(book)
                if incorrect_name != '' or incorrect_year != '' or book_copy != '':
                    add_confirm = messagebox.askyesno('MyLib', f'В файле обнаружены '
                                                               f'следующие ошибки:\n\n'
                                                               f'{incorrect_year}'
                                                               f'{incorrect_name}'
                                                               f'{book_copy}\n'
                                                               f'Игнорировать эти '
                                                               f'позиции и продолжить загрузку? ')
                    if add_confirm:
                        cursor.executemany("INSERT INTO books VALUES (?, ?, ?)", new_books)
                        db.commit()
                        messagebox.showinfo('MyLib', 'Книги успешно добавлены в библиотеку')
                else:
                    cursor.executemany("INSERT INTO books VALUES (?, ?, ?)", new_books)
                    db.commit()
                    messagebox.showinfo('MyLib', 'Книги успешно добавлены в библиотеку')
        except FileNotFoundError:
            pass
        except TypeError:
            pass

    def adding(self):
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
            if res not in cursor.execute("SELECT * FROM books"):
                messagebox.showinfo('MyLib', f'Книга \'{res[2]}\' успешно '
                                             f'добавлена в библиотеку')
                cursor.execute("INSERT INTO books VALUES (?, ?, ?)", res)
                db.commit()
                self.window.destroy()
                AddBook(self.parent)
            else:
                messagebox.showinfo('MyLib', f'Книга \'{res[2]}\' '
                                             f'уже имеется в библиотеке')


class SearchBook(BookForm):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    @property
    def header(self):
        return Label(self.top_frame, text='Введите параметры искомых книг',
                     font=('TimesNewRoman', 15), pady='20', padx='10')

    @property
    def action_button(self):
        return Button(self.bottom_frame, text='Найти', background="#555", foreground="#ccc",
                      padx="70", font=('TimesNewRoman', 13), command=self.searching_result_window)

    def searching_result_window(self):
        SearchingResults(self.book_year_field.get(), self.book_author_field.get(), self.book_name_field.get())


class SearchingResults:
    def __init__(self, book_year=None, book_author=None, book_name=None):
        self.res_search = (book_year, book_author, book_name)
        if self.res_search == ('', '', ''):
            select_ = "SELECT * FROM books"
        else:
            select_ = "SELECT * FROM books WHERE "
            if self.res_search[0].strip() != '':
                if len(select_) == 26:
                    select_ += f"year = '{self.res_search[0]}'"
                else:
                    select_ += f" and year = '{self.res_search[0]}'"
            if self.res_search[1].strip() != '':
                if len(select_) == 26:
                    select_ += f"author = '{self.res_search[1]}'"
                else:
                    select_ += f" and author = '{self.res_search[1]}'"
            if self.res_search[2].strip() != '':
                if len(select_) == 26:
                    select_ += f"name = '{self.res_search[2]}'"
                else:
                    select_ += f" and name = '{self.res_search[2]}'"
        cursor.execute(select_)
        self.book_list = set(Book(*args) for args in cursor.fetchall())

        self.window = Tk()
        self.top_frame = Frame(self.window)
        self.left_frame = Frame(self.window)
        self.right_frame = Frame(self.window)
        self.window.title('Результаты поиска | MyLib')
        self.book_searched_text = Label(self.top_frame, text='Найденные книги:',
                                        font=('TimesNewRoman', 15), pady='20', padx='10')
        self.button_load_txt = Button(self.right_frame, text='Выгрузить в txt',
                                      background="#555", foreground="#ccc",
                                      padx="54", font=('TimesNewRoman', 13), command=self.load_txt)
        self.button_load_json = Button(self.right_frame, text='Выгрузить в json',
                                       background="#555", foreground="#ccc",
                                       padx="48", font=('TimesNewRoman', 13), command=self.load_json)
        self.button_load_csv = Button(self.right_frame, text='Выгрузить в csv',
                                      background="#555",
                                      foreground="#ccc", padx="51",
                                      font=('TimesNewRoman', 13), command=self.load_csv)
        self.button_upd = Button(self.right_frame, text='Изменить',
                                 background="#555", foreground="#ccc",
                                 padx="75", font=('TimesNewRoman', 13), command=self.upd_window)
        self.button_del = Button(self.right_frame, text='Удалить', background="#555",
                                 foreground="#ccc",
                                 padx="80", font=('TimesNewRoman', 13), command=self.del_)

        self.window.geometry('700x500')
        self.top_frame.pack(side='top')
        self.left_frame.pack(side='left', fill='both', expand=True)
        self.right_frame.pack(side='right')
        self.book_searched_text.pack(fill='both')
        self.button_load_txt.grid(sticky='e')
        self.button_load_csv.grid(sticky='e')
        self.button_load_json.grid(sticky='e')
        self.button_upd.grid(sticky='e')
        self.button_del.grid(sticky='e')
        self.table = ttk.Treeview(self.left_frame, columns=("year", "author", "name"), height=500)
        self.table.column("#0", width=40, minwidth=40, stretch='no')
        self.table.column("year", width=100, stretch='no')
        self.table.column("author", width=150, stretch='no')
        self.table.column("name", width=150, stretch='yes')
        self.table.heading("#0", text="#", anchor='w')
        self.table.heading("year", text="Год издания", anchor='w')
        self.table.heading("author", text="Автор", anchor='w')
        self.table.heading("name", text="Название", anchor='w')

        for num, book in enumerate(self.book_list, 1):
            self.table.insert("", num, text=f"{num}", values=(book.year, book.author, book.name))

        self.table.pack(side='top', fill='x')
        self.left_frame.mainloop()

    def upd_window(self):
        try:
            item = self.table.selection()[0]
            book_info_to_update = self.table.item(item, 'values')
            UpdateBook(self, book_info_to_update)
        except IndexError:
            messagebox.showinfo('MyLib', 'Не выбрано ни одной книги')

    def del_(self):
        """
        Удалить книгу из базы данных
        """
        item = self.table.selection()
        if not item:
            messagebox.showinfo('MyLib', 'Не выбрано ни одной книги')
        else:
            del_confirm = messagebox.askyesno('MyLib', 'Удалить выбранные книги '
                                                       'из базы данных?')
            if del_confirm:
                for i in item:
                    book_info = self.table.item(i, 'values')
                    cursor.execute("DELETE FROM books WHERE year = (?) "
                                   "and author = (?) and name = (?)", book_info)
                    db.commit()
                    self.table.delete(i)
                messagebox.showinfo('MyLib', 'Выбранные книги удалены')

    def load_txt(self):
        """
        Выгрузить список книг в TXT
        """
        with open('book_list.txt', "w", encoding='utf-8') as f_txt:
            for ind, book in enumerate(self.book_list, 1):
                f_txt.write(f"{ind}. Год выпуска: "
                            f"{book[0] if book[0] != '' else 'не указан'}, "
                            f"Автор: {book[1] if book[1] != '' else 'не указан'}, "
                            f"Название: {book[2]}\n")
        messagebox.showinfo('MyLib', 'Список книг выгружен в файл book_list.txt')

    def load_csv(self):
        """
        Выгрузить список книг в таблицу CSV
        """
        with open('book_table.csv', "w", encoding='utf-8') as f_csv:
            writer = csv.writer(f_csv, delimiter=',', lineterminator="\r")
            for book in self.book_list:
                writer.writerow(book)
        messagebox.showinfo('MyLib', 'Список книг выгружен в файл book_table.csv')

    def load_json(self):
        """
        Выгрузить список книг в JSON
        """
        with open('book_list.json', "w", encoding='utf-8') as f_json:
            list_of_books = []
            for ind, book in enumerate(self.book_list, 1):
                data = {
                    "Год выпуска": f"{book[0] if book[0] != '' else 'не указан'}",
                    "Автор": f"{book[1] if book[1] != '' else 'не указан'}",
                    "Название": f"{book[2]}"
                }
                list_of_books.append(data)
            json.dump(list_of_books, f_json, ensure_ascii=False)
        messagebox.showinfo('MyLib', 'Список книг выгружен в файл book_list.json')


class UpdateBook(BookForm):
    def __init__(self, parent, chosen_book):
        super().__init__(parent, chosen_book)
        self.book_info_to_update = chosen_book
        self.parent = parent

    @property
    def header(self):
        return Label(self.top_frame, text='Внесите изменения',
                     font=('TimesNewRoman', 15), pady='20', padx='10')

    @property
    def action_button(self):
        return Button(self.bottom_frame, text='Применить', background="#555", foreground="#ccc",
                      padx="70", font=('TimesNewRoman', 13), command=self.accept_changes)

    def accept_changes(self):
        """
        Функция, принимаюшая и сохраняющая изменения
        :return:
        """
        res_upd = (self.book_year_field.get(), self.book_author_field.get(), self.book_name_field.get())
        if res_upd[0] and not res_upd[0].isdigit():
            self.book_year_text.configure(text='Год издания (необходимо указать год в числовом формате):',
                                          fg='red')
            res_upd = ('', '', '')
        if not res_upd[2]:
            self.book_name_text.configure(text='Название (это поле обязательно для заполнения):',
                                          fg='red')
            res_upd = ('', '', '')
        if res_upd != ('', '', ''):
            if res_upd not in cursor.execute("SELECT * FROM books"):
                query = f"UPDATE books SET year = '{res_upd[0]}', " \
                        f"author = '{res_upd[1].strip()}', " \
                        f"name = '{res_upd[2]}' " \
                        f"WHERE year = '{self.book_info_to_update[0]}' and " \
                        f"author = '{self.book_info_to_update[1]}'" \
                        f" and name = '{self.book_info_to_update[2]}'"
                cursor.execute(query)
                db.commit()
                messagebox.showinfo('MyLib', 'Информация о книге была изменена')
                self.window.destroy()
                self.parent.window.destroy()
                SearchingResults(*self.parent.res_search)
            else:
                messagebox.showinfo('MyLib', f'Книга \'{res_upd[2]}\''
                                             f' уже имеется в библиотеке')

    def closing(self):
        """
        Завершение работы программы
        :return:
        """
        self.window.destroy()


main_window = MainMenu()
db.close()
