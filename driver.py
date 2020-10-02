import json
import csv
from abc import abstractmethod, ABC

from tkinter import messagebox

class IStructureDriver(ABC):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, d):
        pass


class JsonFileDriver(IStructureDriver):
    def __init__(self, filename):
        self.__filename = filename

    def read(self):
        with open(self.__filename, 'r', encoding='utf8') as f:
            return json.load(f)

    def write(self, some_data=None):
        with open('book_list.json', "w", encoding='utf-8') as f_json:
            list_of_books = []
            for ind, book in enumerate(some_data, 1):
                data = {
                    "Год выпуска": f"{book[0] if book[0] != '' else 'не указан'}",
                    "Автор": f"{book[1] if book[1] != '' else 'не указан'}",
                    "Название": f"{book[2]}"
                }
                list_of_books.append(data)
            json.dump(list_of_books, f_json, ensure_ascii=False)
        messagebox.showinfo('MyLib', f'Список книг выгружен в файл {self.__filename}')


class CSVFileDriver(IStructureDriver):
    def __init__(self, filename):
        self.__filename = filename

    def read(self):
        with open(self.__filename, 'r', encoding='utf8') as f:
            file_reader = csv.reader(f, delimiter = ",")
            file_reader = list(file_reader)
            return file_reader

    def write(self, some_data=None):
        with open('book_table.csv', "w", encoding='utf-8') as f_csv:
            writer = csv.writer(f_csv, delimiter=',', lineterminator="\r")
            for book in some_data:
                writer.writerow(book)
        messagebox.showinfo('MyLib', f'Список книг выгружен в файл {self.__filename}')

