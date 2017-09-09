class BaseCMD:
    def __init__(self, args):
        self.name = self.__class__.__name__.rsplit('CMD')
        self.args = args

    def do(self):
        raise NotImplementedError

SUB_COMMANDS = {'meal_log': 'meal_log',
                'my_foods': 'my_foods',
                'stofc2015r7': 'stofc2015r7',  # 日本食品標準成分表2015年版（七訂）の変換
                }
