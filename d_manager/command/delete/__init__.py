from d_manager.command import BaseCommand
from d_manager.command.delete.product_food import DeelteProductFoodCommand

TARGETS = {'product_food': DeelteProductFoodCommand,
           }


class Delete(BaseCommand):
    def __init__(self, args):
        self.__args = args

    def do(self):
        if self.__args[0] in TARGETS.keys():
            target = self.__args[0]
            args = self.__args[1:]
            TARGETS[target](args).do()
        else:
            raise Exception()
