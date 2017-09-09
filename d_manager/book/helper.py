class InteractiveHelper:
    """対話的に値を読み込む各種メソッドを提供する"""
    @staticmethod
    def get_value(checker, caster):
        """値を対話的に得る"""
        err_msg = '不正な入力値。'
        # プロンプトによる入力と、入力値の確認
        while True:
            i = input('?> ')
            if i and checker(i):
                try:
                    i = caster(i)
                    print('{} が入力されました。\n'.format(i))
                    return i
                except ValueError:
                    print(err_msg)
            else:
                print(err_msg)

    @classmethod
    def get_str(cls):
        """文字列を対話的に得る"""
        return cls.get_value(lambda x: True, lambda x: x)

    @classmethod
    def get_integer(cls):
        """整数値を対話的に読み込む"""
        return cls.get_value(lambda x: x.isdecimal(), lambda x: int(x))

    @classmethod
    def get_float(cls):
        """動点小数点数を対話的に読み込む"""
        return cls.get_value(lambda x: True, lambda x: float(x))

    @staticmethod
    def choose_from_dict(choice_dict, fold=4, sep=','):
        """与えられた辞書形式の選択肢から一つ選ばせる。"""
        msg = ''
        i = 0
        for key, value in choice_dict.items():
            if (i % fold) == 0:
                msg += '\n'

            msg += ' {}: {}{}'.format(key, value, sep)
            i += 1
            if i == len(choice_dict.values()):
                msg = msg.rstrip(sep)
        else:
            msg += '\n'
            print(msg)

        # 型変換準備
        type_of_key = type(list(choice_dict.keys())[0])

        # プロンプトによる入力と、入力値の確認
        while True:
            _input = input('?> ')
            try:
                key = type_of_key(_input)
            except ValueError:
                print('不正な入力値。')
                continue

            if key in choice_dict.keys():
                choice = choice_dict[key]
                print('{}: {} が選択されました。\n'.format(key, choice))
                # key も返す
                return key, choice
            else:
                print('不正な入力値。選択肢の範囲外が選択されました。')

    @classmethod
    def choose_from_list(cls, choice_list, fold=4, sep=','):
        """与えられたリスト形式の選択肢から一つ選ばせる。"""
        # 採番して辞書に変換してから選ばせる。
        cdict = dict()
        key = 1
        for value in choice_list:
            cdict[key] = value
            key += 1
        else:
            return cls.choose_from_dict(cdict, fold, sep)

    @staticmethod
    def confirm_yes_of_no():
        """Yes か No の二択で確認する"""
        while True:
            _input = input('[Y/n]> ')
            if _input in ('Y', 'Yes', 'yes'):
                return True
            elif _input in ('n', 'No', 'no'):
                return False
            else:
                print('不正な入力値。')
                continue
