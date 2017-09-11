import pickle


class PickleBookWriter:
    def __init__(self, file, mode='wb'):
        self.__file = file
        self.__mode = mode

    def write(self, book):
        with open(self.__file, mode=self.__mode) as f:
            pickle.dump(book, f)
