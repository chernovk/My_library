from abc import abstractmethod, ABC
from driver import JsonFileDriver
from driver import CSVFileDriver
from tkinter import *


class Builder(ABC):
    def __init__(self):
        self.window = Tk()
        self.file_name = Entry(self.window, width=40)
        self.window.title('Введите название файла | MyLib')
        self.header = Label(self.window, text='Введите название файла',
                            font=('TimesNewRoman', 15), pady='20', padx='10')
        self.action_button = Button(self.window, text='Применить', background="#555", foreground="#ccc",
                                    padx="70", font=('TimesNewRoman', 13), command=self.build)

        self.header.pack(fill='both')
        self.file_name.pack()
        self.file_name.focus()
        self.action_button.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.closing)
        self.window.mainloop()

    @abstractmethod
    def build(self):
        pass

    def closing(self):
        """
        Завершение работы программы
        :return:
        """
        self.window.destroy()


class JsonBuilder(Builder):
    def __init__(self):
        super().__init__()

    def build(self, filename=None):
        filename = self.file_name.get()
        if not filename:
            filename = 'tmp.json'
        else:
            filename = filename.strip()
            if not filename.endswith('.json'):
                filename = filename + '.json'

        return JsonFileDriver(filename)


class CSVBuilder(Builder):

    def build(self):
        filename = self.file_name.get()
        if not filename:
            filename = 'tmp.csv'
        else:
            filename = filename.strip()
            if not filename.endswith('.csv'):
                filename = filename + '.csv'

        return CSVFileDriver(filename)


class DriverFactory:

    @staticmethod
    def get_driver(driver_name):
        drivers = {
            'json': JsonBuilder,
            'csv': CSVBuilder
        }
        if driver_name in drivers:
            return drivers[driver_name]().build()


if __name__ == '__main__':

    JsonBuilder();