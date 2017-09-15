from d_manager.command import BaseCommand
from d_manager.command.view.product_food import ViewProductFoodPickleFileCommand
from d_manager.command.view.stofc2015_food import ViewSTOFC2015PickleFileCommand
from d_manager.command.view.meal import ViewMealLogPickleFileCommand

TARGETS = {'meal': ViewMealLogPickleFileCommand,
           'product_food': ViewProductFoodPickleFileCommand,
           'stofc2015_food': ViewSTOFC2015PickleFileCommand,
           }


class View(BaseCommand):
    def __init__(self, args):
        self.__args = args

    def do(self):
        if self.__args[0] in TARGETS.keys():
            target = self.__args[0]
            args = self.__args[1:]
            TARGETS[target](args).do()
        else:
            raise Exception()
