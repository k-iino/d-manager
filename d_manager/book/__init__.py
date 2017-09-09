class Book:
    def __init__(self, loader=None, dumper=None, entries=None):
        if entries:
            self.__entries = entries
        else:
            self.__entries = dict()

        self.__loader = loader
        self.__dumper = dumper

    def set_loader(self, loader):
        self.__loader = loader

    def set_dumper(self, dumper):
        self.__dumper = dumper

    def load(self):
        self.__loader.load(self.__entries)

    def dump(self):
        self.__dumper.dump(self.__entries)
