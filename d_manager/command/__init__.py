class BaseCMD:
    def __init__(self, args):
        self.name = self.__class__.__name__.rsplit('CMD')
        self.args = args

    def do(self):
        raise NotImplementedError
