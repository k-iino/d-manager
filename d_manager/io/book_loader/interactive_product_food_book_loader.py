import yaml

from d_manager.helper.prompt_helper import PromptHelper as Helper
from d_manager.food import FOOD_GROUPS
from d_manager.food.product_food import ProductFood


class InteractiveProductFoodBookLoader:
    """対話的に市販食品を読み込む"""
    food_energy_unit = 'kcal'
    food_mass_unit = 'gram'

    def __load(self, book):
        # 食品分類
        #
        # 日本食品標準成分表 2015 に収載されている食品群から選択
        Helper.print_msg('食品のグループを番号で選択してください。')
        group_number, group_name = Helper.choose_from_dict(FOOD_GROUPS)

        #
        # 「一括表示」部分（商品名および名称など）の入力
        #
        # 参考
        #   加工食品品質表示基準改正（わかりやすい表示方法等）に関するQ&A｜消費者庁 - http://www.caa.go.jp/foods/qa/kakou04_qa.html#a09

        # 食品の名称と商品名は異なる。
        Helper.print_msg('食品の「商品名」を入力してください。', '注意: 一括表示内の「名称」のことではなく「商品名」です。')
        product_name = Helper.get_str()
        # また、名称の記載は義務だが、商品名の近くに記載してある場合は、一括表示欄に記載しなくてもよい。
        Helper.print_msg('食品の「名称」を入力してください。', '注意: 包装内の一括表示内の「名称」欄に記載されているものです。')
        food_name = Helper.get_str()

        # 製造所の所在地及び製造者の氏名又は名称
        Helper.print_msg('製造者の氏名又は名称を入力してください。',
                         '備考: 包装内の一括表示内の「製造者」欄に記載されているもの。',
                         '     複数記載されている場合、は最初に記載されているものを採用すること。')
        make_name = Helper.get_str()

        #
        # 「栄養成分表示」
        #
        # 食品単位は、100g、100ml、１食分、１包装その他の１単位のいずれか（食品表示法）
        dimensionless_unit = 'dimensionless'
        nutrient_units = ['100g', '100ml', '1' + dimensionless_unit]
        Helper.print_msg('栄養成分表示の食品単位を入力してください。',
                         '食品単位は、栄養成分表示の基準となる量で 100g、100ml、もしくはその他の1単位で表記されています。',
                         '注意: 商品の内容量ではないので注意。')
        _, nutrient_declaration_unit = Helper.choose_from_list(nutrient_units)
        # 栄養成分表示の食品単位の物理量
        if nutrient_declaration_unit == '1' + dimensionless_unit:
            # 食品単位が1単位（１杯、１食分、１包装など）のどれかの場合は、
            # その1単位の物理量を明示的に指定する必要がある。
            Helper.print_msg('食品の1単位（１杯、１食分、１包装など）の物理量を記入してください。',
                             '栄養成分表示の食品単位に併記されている物理量を記入してくだい。'
                             ''
                             '量の単位を以下から選択してください。')
            # 食品1単位（１杯、１食分、１包装など）の物理量の単位
            one_packet_units = ['kg', 'g', 'ml', 'l']
            _, _unit = Helper.choose_from_list(one_packet_units)
            Helper.print_msg('量の数値を記入してください。')
            _quantity = str(Helper.get_float())
            food_amount = ''.join((_quantity, _unit))
        else:
            # 食品単位が物理量だった場合はそれをそのまま利用する
            food_amount = nutrient_declaration_unit

        # 栄養成分表示の食品単位ごとの値
        # 各栄養素の単位は以下のガイドラインを参考にした。
        # 「食品表示法に基づく栄養成分表示のためのガイドライン 第1版 平成27年3月」
        #  http://www.caa.go.jp/foods/pdf/150331_GL-nutrition.pdf
        Helper.print_msg('栄養成分表示の入力',
                         '食品単位ごとの値です。入力された食品単位={}'.format(nutrient_declaration_unit))
        # 熱量
        Helper.print_msg('カロリーを入力してください。単位={}'.format(self.food_energy_unit))
        energy = str(Helper.get_integer()) + self.food_energy_unit
        # タンパク質
        Helper.print_msg('タンパク質を入力してください。単位={}'.format(self.food_mass_unit))
        protein = str(Helper.get_float()) + self.food_mass_unit
        # 脂質
        Helper.print_msg('脂質を入力してください。単位={}'.format(self.food_mass_unit))
        lipid = str(Helper.get_float()) + self.food_mass_unit
        # 炭水化物
        Helper.print_msg('炭水化物を入力してください。単位={}'.format(self.food_mass_unit))
        carbohydrate = str(Helper.get_float()) + self.food_mass_unit
        # 食塩相当量
        Helper.print_msg('食塩相当量を入力してください。単位={}'.format(self.food_mass_unit))
        salt = str(Helper.get_float()) + self.food_mass_unit

        #
        # 食品情報の生成
        #
        product_food = ProductFood(maker_name=make_name,
                                   product_name=product_name,
                                   food_name=food_name,
                                   amount=food_amount)
        product_food.set_nutrients_list([energy,
                                         protein,
                                         lipid,
                                         carbohydrate,
                                         salt
                                         ])

        # 登録
        Helper.print_msg('以下をグループ「{}」登録しますが、よろしいですか？'.format(FOOD_GROUPS[group_number]))
        print(yaml.dump(product_food.to_dict()))
        if Helper.confirm_yes_of_no():
            _id = book.append(product_food, group_number)
            print('グループ内の ID:{} として登録されました。'.format(_id))
        else:
            print('登録がキャンセルされました。')

    def load(self, book):
        """対話的に食品を読み込む"""
        while True:
            self.__load(book)
            Helper.print_msg('引き続き登録しますか？')
            if not Helper.confirm_yes_of_no():
                break
