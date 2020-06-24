"""
Данный модуль представляет собой электронную библиотеку с графическим интерфейсом,
реализованный с помощью tkinter и базы данных sqlite3.  При реализации несколько раз думал,
что очень кстати пришлось бы знание классов и ООП, но пока только так.
"""


import csv
from typing import NoReturn

import sqlite3
import tkinter
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog


db = sqlite3.connect('biblioteka.db')
sql = db.cursor()
sql.execute('''CREATE TABLE IF NOT EXISTS books (
    year TEXT,
    author TEXT,
    name TEXT
    )''')
db.commit()

main_window = tkinter.Tk()
main_window.title('Моя Библиотека | MyLib')
top_frame_mw = tkinter.Frame(main_window)
top_frame_mw.pack()

bottom_frame_mw = tkinter.Frame(main_window)
bottom_frame_mw.pack(side='bottom')
greetings_text = tkinter.Label(top_frame_mw, text='Добро пожаловать в библиотеку MyLib',
                               font=('TimesNewRoman', 16), pady='20', padx='20')
greetings_text.pack(fill='both')


def searching_window() -> NoReturn:
    """
    Функция-окно поиска книги
    :return:
    """
    main_window.withdraw()
    search_window = tkinter.Tk()
    search_window.title('Поиск / Удаление / Редактирование книги | MyLib')

    top_frame_sw = tkinter.Frame(search_window)
    top_frame_sw.pack()

    bottom_frame_sw = tkinter.Frame(search_window)
    bottom_frame_sw.pack(side='bottom')

    left_frame_sw = tkinter.Frame(search_window)
    left_frame_sw.pack(side='left')

    right_frame_sw = tkinter.Frame(search_window)
    right_frame_sw.pack(side='right', fill='x', expand=True)

    book_search_text = tkinter.Label(top_frame_sw, text='Введите параметры искомых книг',
                                     font=('TimesNewRoman', 15), pady='20', padx='10')
    book_search_text.pack(fill='both')

    book_year_text_s = tkinter.Label(left_frame_sw, text='Год издания:', font=('TimesNewRoman', 13))
    book_year_text_s.grid()
    book_year_s = tkinter.Entry(right_frame_sw, width=40)
    book_year_s.pack(fill='x', expand=True)
    book_year_s.focus()

    book_author_text_s = tkinter.Label(left_frame_sw, text='Автор:', font=('TimesNewRoman', 13))
    book_author_text_s.grid()
    book_author_s = tkinter.Entry(right_frame_sw, width=40)
    book_author_s.pack(fill='x', expand=True)

    book_name_text_s = tkinter.Label(left_frame_sw, text='Название:', font=('TimesNewRoman', 13))
    book_name_text_s.grid()
    book_name_s = tkinter.Entry(right_frame_sw, width=40)
    book_name_s.pack(fill='x', expand=True)

    def backing() -> NoReturn:
        """
        функция для кнопки "Назад(домой)"
        :return:
        """
        search_window.destroy()
        main_window.deiconify()

    button_back = tkinter.Button(bottom_frame_sw, text='Назад', background="#555",
                                 foreground="#ccc", padx="70",
                                 font=('TimesNewRoman', 13), command=backing)
    button_back.pack(side='left')

    def searching() -> NoReturn:
        """
        Функция-окно результатов поиска
        :return:
        """
        res_search = (book_year_s.get(), book_author_s.get(), book_name_s.get())
        if res_search == ('', '', ''):
            select_ = "SELECT * FROM books"
        else:
            select_ = "SELECT * FROM books WHERE "
            if res_search[0].strip() != '':
                if len(select_) == 26:
                    select_ += f"year = '{res_search[0]}'"
                else:
                    select_ += f" and year = '{res_search[0]}'"
            if res_search[1].strip() != '':
                if len(select_) == 26:
                    select_ += f"author = '{res_search[1]}'"
                else:
                    select_ += f" and author = '{res_search[1]}'"
            if res_search[2].strip() != '':
                if len(select_) == 26:
                    select_ += f"name = '{res_search[2]}'"
                else:
                    select_ += f" and name = '{res_search[2]}'"
        sql.execute(select_)
        book_list = set(sql.fetchall())

        if len(book_list) > 0:
            searched_window = tkinter.Tk()
            searched_window.title('Результаты поиска | MyLib')
            searched_window.geometry('700x500')

            top_frame_sdw = tkinter.Frame(searched_window)
            top_frame_sdw.pack(side='top')

            left_frame_sdw = tkinter.Frame(searched_window)
            left_frame_sdw.pack(side='left', fill='both', expand=True)

            right_frame_sdw = tkinter.Frame(searched_window)
            right_frame_sdw.pack(side='right')

            def upd_() -> NoReturn:
                """
                Функция-окно внесения изменений
                :return:
                """
                try:
                    item = table.selection()[0]
                    book_info_to_update = table.item(item, 'values')

                    upd_window = tkinter.Tk()
                    upd_window.title('Изменение книги | MyLib')

                    top_frame_uw = tkinter.Frame(upd_window)
                    top_frame_uw.pack(side='top')

                    bottom_frame_uw = tkinter.Frame(upd_window)
                    bottom_frame_uw.pack(side='bottom')

                    left_frame_uw = tkinter.Frame(upd_window)
                    left_frame_uw.pack(side='left')

                    right_frame_uw = tkinter.Frame(upd_window)
                    right_frame_uw.pack(side='right', fill='x', expand=True)

                    book_upd_text = tkinter.Label(top_frame_uw, text='Внесите изменения',
                                                  font=('TimesNewRoman', 15), pady='20', padx='10')
                    book_upd_text.pack(fill='both')

                    book_year_text_u = tkinter.Label(left_frame_uw, text='Год издания:',
                                                     font=('TimesNewRoman', 13))
                    book_year_text_u.grid()
                    book_year_u = tkinter.Entry(right_frame_uw, width=40)
                    book_year_u.pack(fill='x', expand=True)
                    book_year_u.focus()

                    book_author_text_u = tkinter.Label(left_frame_uw, text='Автор:',
                                                       font=('TimesNewRoman', 13))
                    book_author_text_u.grid()
                    book_author_u = tkinter.Entry(right_frame_uw, width=40)
                    book_author_u.pack(fill='x', expand=True)

                    book_name_text_u = tkinter.Label(left_frame_uw, text='Название:',
                                                     font=('TimesNewRoman', 13))
                    book_name_text_u.grid()
                    book_name_u = tkinter.Entry(right_frame_uw, width=40)
                    book_name_u.pack(fill='x', expand=True)

                    book_year_u.insert(0, book_info_to_update[0])
                    book_author_u.insert(0, book_info_to_update[1])
                    book_name_u.insert(0, book_info_to_update[2])

                    def cancel() -> NoReturn:
                        """
                        функция для кнопки "Назад(домой)"
                        :return:
                        """
                        upd_window.destroy()

                    def accept() -> NoReturn:
                        """
                        Функция, принимаюшая изменения
                        :return:
                        """
                        res_upd = (book_year_u.get(), book_author_u.get(), book_name_u.get())
                        if res_upd[0] and not res_upd[0].isdigit():
                            book_year_text_u.configure(text='Год издания (необходимо '
                                                            'указать год в числовом формате):',
                                                       fg='red')
                            res_upd = ('', '', '')
                        if not res_upd[2]:
                            book_name_text_u.configure(text='Название (это поле '
                                                            'обязательно для заполнения):',
                                                       fg='red')
                            res_upd = ('', '', '')
                        if res_upd != ('', '', ''):
                            if res_upd not in sql.execute("SELECT * FROM books"):
                                query = f"UPDATE books SET year = '{res_upd[0]}', " \
                                        f"author = '{res_upd[1].strip()}', " \
                                        f"name = '{res_upd[2]}' " \
                                        f"WHERE year = '{book_info_to_update[0]}' and " \
                                        f"author = '{book_info_to_update[1]}'" \
                                        f" and name = '{book_info_to_update[2]}'"
                                sql.execute(query)
                                db.commit()
                                messagebox.showinfo('MyLib', 'Информация о книге была изменена')
                                upd_window.destroy()
                                searched_window.destroy()
                                searching()
                            else:
                                messagebox.showinfo('MyLib', f'Книга \'{res_upd[2]}\''
                                                             f' уже имеется в библиотеке')

                    button_cancel = tkinter.Button(bottom_frame_uw, text='Отмена',
                                                   background="#555", foreground="#ccc",
                                                   padx="70", font=('TimesNewRoman', 13),
                                                   command=cancel)
                    button_cancel.pack(side='left')

                    button_accept = tkinter.Button(bottom_frame_uw, text='Применить',
                                                   background="#555", foreground="#ccc", padx="70",
                                                   font=('TimesNewRoman', 13), command=accept)
                    button_accept.pack(side='left')
                except IndexError:
                    messagebox.showinfo('MyLib', 'Не выбрано ни одной книги')

            def del_() -> NoReturn:
                """
                Удалить книгу из базы данных
                """
                item = table.selection()
                if not item:
                    messagebox.showinfo('MyLib', 'Не выбрано ни одной книги')
                else:
                    del_confirm = messagebox.askyesno('MyLib', 'Удалить выбранные книги '
                                                               'из базы данных?')
                    if del_confirm:
                        for i in item:
                            book_info = table.item(i, 'values')
                            sql.execute("DELETE FROM books WHERE year = (?) "
                                        "and author = (?) and name = (?)", book_info)
                            db.commit()
                            table.delete(i)
                        messagebox.showinfo('MyLib', 'Выбранные книги удалены')

            def load_txt() -> NoReturn:
                """
                Выгрузить список книг в TXT
                """
                with open('book_list.txt', "w") as f_txt:
                    for ind, book in enumerate(book_list, 1):
                        f_txt.write(f"{ind}. Год выпуска: "
                                    f"{book[0] if book[0] != '' else 'не указан'}, "
                                    f"Автор: {book[1] if book[1] != '' else 'не указан'}, "
                                    f"Название: {book[2]}\n")
                messagebox.showinfo('MyLib', 'Список книг выгружен в файл book_list.txt')

            def load_csv() -> NoReturn:
                """
                Выгрузить список книг в таблицу CSV
                """
                with open('book_table.csv', "w") as f_csv:
                    writer = csv.writer(f_csv, delimiter=',')
                    for book in book_list:
                        writer.writerow(book)
                messagebox.showinfo('MyLib', 'Список книг выгружен в файл book_table.csv')

            book_searched_text = tkinter.Label(top_frame_sdw, text='Найденные книги:',
                                               font=('TimesNewRoman', 15), pady='20', padx='10')
            book_searched_text.pack(fill='both')
            button_load = tkinter.Button(right_frame_sdw, text='Выгрузить в txt',
                                         background="#555", foreground="#ccc",
                                         padx="54", font=('TimesNewRoman', 13), command=load_txt)
            button_load.grid(sticky='e')

            button_load_csv = tkinter.Button(right_frame_sdw, text='Выгрузить в csv',
                                             background="#555",
                                             foreground="#ccc", padx="51",
                                             font=('TimesNewRoman', 13), command=load_csv)
            button_load_csv.grid(sticky='e')

            button_upd = tkinter.Button(right_frame_sdw, text='Изменить',
                                        background="#555", foreground="#ccc",
                                        padx="75", font=('TimesNewRoman', 13), command=upd_)
            button_upd.grid(sticky='e')

            button_del = tkinter.Button(right_frame_sdw, text='Удалить', background="#555",
                                        foreground="#ccc",
                                        padx="80", font=('TimesNewRoman', 13), command=del_)
            button_del.grid(sticky='e')

            table = ttk.Treeview(left_frame_sdw, columns=("year", "author", "name"), height=500)

            table.column("#0", width=40, minwidth=40, stretch='no')
            table.column("year", width=100, stretch='no')
            table.column("author", width=150, stretch='no')
            table.column("name", width=150, stretch='yes')

            table.heading("#0", text="#", anchor='w')
            table.heading("year", text="Год издания", anchor='w')
            table.heading("author", text="Автор", anchor='w')
            table.heading("name", text="Название", anchor='w')

            for num, row in enumerate(book_list, 1):
                table.insert("", num, text=f"{num}", values=row)

            table.pack(side='top', fill='x')
            left_frame_sdw.mainloop()
        else:
            messagebox.showinfo('MyLib', 'Книги, соответствующие'
                                         ' выбранным параметрам отсутствуют')

    button_search = tkinter.Button(bottom_frame_sw, text='Найти',
                                   background="#555", foreground="#ccc",
                                   padx="70", font=('TimesNewRoman', 13), command=searching)
    button_search.pack(side='right')

    def closing() -> NoReturn:
        """
        Завершение работы программы
        :return:
        """
        if messagebox.askokcancel("MyLib", "Завершить работу в MyLib?"):
            search_window.destroy()
            main_window.destroy()
            db.close()

    search_window.protocol("WM_DELETE_WINDOW", closing)
    search_window.mainloop()


def adding_window() -> NoReturn:
    """
    Функция-окно добавления книг
    :return:
    """
    main_window.withdraw()
    add_window = tkinter.Tk()
    add_window.title('Добавление книги | MyLib')

    top_frame_aw = tkinter.Frame(add_window)
    top_frame_aw.pack(side='top')

    bottom_frame_aw = tkinter.Frame(add_window)
    bottom_frame_aw.pack(side='bottom')

    left_frame_aw = tkinter.Frame(add_window)
    left_frame_aw.pack(side='left')

    right_frame_aw = tkinter.Frame(add_window)
    right_frame_aw.pack(side='right', fill='x', expand=True)

    book_add_text = tkinter.Label(top_frame_aw, text='Введите данные о '
                                                     'добавляемой книге',
                                  font=('TimesNewRoman', 15), pady='20', padx='10')
    book_add_text.pack(fill='both')

    book_year_text = tkinter.Label(left_frame_aw, text='Год издания:',
                                   font=('TimesNewRoman', 13))
    book_year_text.grid()
    book_year = tkinter.Entry(right_frame_aw, width=40)
    book_year.pack(fill='x', expand=True)
    book_year.focus()

    book_author_text = tkinter.Label(left_frame_aw, text='Автор:',
                                     font=('TimesNewRoman', 13))
    book_author_text.grid()
    book_author = tkinter.Entry(right_frame_aw, width=40)
    book_author.pack(fill='x', expand=True)

    book_name_text = tkinter.Label(left_frame_aw, text='Название:',
                                   font=('TimesNewRoman', 13))
    book_name_text.grid()
    book_name = tkinter.Entry(right_frame_aw, width=40)
    book_name.pack(fill='x', expand=True)

    def backing() -> NoReturn:
        """
        функция для кнопки "Назад(домой)"
        :return:
        """
        add_window.destroy()
        main_window.deiconify()

    button_back = tkinter.Button(bottom_frame_aw, text='Назад',
                                 background="#555", foreground="#ccc",
                                 padx="70", font=('TimesNewRoman', 13), command=backing)
    button_back.pack(side='left')

    def adding() -> NoReturn:
        """
        добавление одной книги со внесенными параметрами
        :return:
        """
        res = (book_year.get(), book_author.get(), book_name.get())
        if res[0] and not res[0].isdigit():
            book_year_text.configure(text='Год издания (необходимо указать '
                                          'год в числовом формате):', fg='red')
            res = (None, None, None)
        if not res[2]:
            book_name_text.configure(text='Название (это поле обязательно '
                                          'для заполнения):', fg='red')
            res = (None, None, None)
        if res != (None, None, None):
            if res not in sql.execute("SELECT * FROM books"):
                messagebox.showinfo('MyLib', f'Книга \'{res[2]}\' успешно '
                                             f'добавлена в библиотеку')
                sql.execute("INSERT INTO books VALUES (?, ?, ?)", res)
                db.commit()
                add_window.destroy()
                adding_window()
            else:
                messagebox.showinfo('MyLib', f'Книга \'{res[2]}\' '
                                             f'уже имеется в библиотеке')

    button_add = tkinter.Button(bottom_frame_aw, text='Добавить',
                                background="#555", foreground="#ccc",
                                padx="70", font=('TimesNewRoman', 13), command=adding)
    button_add.pack(side='left')

    def add_file() -> NoReturn:
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

    button_add_file = tkinter.Button(bottom_frame_aw, text='Добавить несколько '
                                                           'из файла csv', background="#555",
                                     foreground="#ccc", padx="70",
                                     font=('TimesNewRoman', 13), command=add_file)
    button_add_file.pack(side='bottom')

    def closing() -> NoReturn:
        """
        Завершение работы программы
        :return:
        """
        if messagebox.askokcancel("MyLib", "Завершить работу в MyLib?"):
            add_window.destroy()
            main_window.destroy()
            db.close()

    add_window.protocol("WM_DELETE_WINDOW", closing)
    add_window.mainloop()



button_searching = tkinter.Button(bottom_frame_mw, text='Найти / Удалить / Изменить книги',
                                  background="#555",
                                  foreground="#ccc", padx="135",
                                  font=('TimesNewRoman', 13), command=searching_window)
button_searching.pack(fill='both')
button_adding = tkinter.Button(bottom_frame_mw, text='Добавить книги',
                               background="#555", foreground="#ccc",
                               padx="100", font=('TimesNewRoman', 13),
                               command=adding_window)
button_adding.pack(fill='both')
main_window.mainloop()
db.close()
