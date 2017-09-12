from d_manager.command import BaseCommand
from d_manager.command.add import product_food
from d_manager.command.add import meal_log

TARGETS = {'product_food': product_food.AddProductFoodCommand,
           'meal_log': meal_log.AddMealLogCommand,
           }


class Add(BaseCommand):
    def __init__(self, args):
        self.__args = args

    def do(self):
        if self.__args[0] in TARGETS.keys():
            target = self.__args[0]
            args = self.__args[1:]
        else:
            raise Exception()

        TARGETS[target](args).do()
