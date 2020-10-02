class Book:
    def __init__(self, year, author, name):
        self.year = year  # self.__year = year  over property
        self.__author = author
        self.name = name

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year):
        self.__year = year

    @property
    def author(self):
        return self.__author


if __name__ == '__main__':
    Book(1994, 'test', 'test')