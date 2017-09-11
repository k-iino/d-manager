from d_manager.command import BaseCommand
from d_manager.command.delete import stofc2015_xlsx

TARGETS = {'stofc2015_excel': stofc2015_xlsx.ConvertSTOFC2015ExcelFileCommand,
           }


class Convert(BaseCommand):
    def __init__(self, args):
        self.__args = args

    def do(self):
        if self.__args[0] in TARGETS.keys():
            target = self.__args[0]
            args = self.__args[1:]
            TARGETS[target](args).do()
        else:
            raise Exception()