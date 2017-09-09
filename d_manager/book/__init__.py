class Book:
    def __init__(self, loader=None, dumper=None, deleter=None, entries=None):
        if entries:
            self.__entries = entries
        else:
            self.__entries = dict()

        self.__loader = loader
        self.__dumper = dumper
        self.__deleter = deleter

    def set_loader(self, loader):
        self.__loader = loader

    def set_dumper(self, dumper):
        self.__dumper = dumper
        
    def set_deleter(self, deleter):
        self.__deleter = deleter

    def load(self):
        self.__loader.load(self.__entries)

    def dump(self):
        self.__dumper.dump(self.__entries)

    def delete(self):
        self.__deleter.delete(self.__entries)
