from d_manager.food.product_food import ProductFood
from d_manager.book.product_food_book import GROUPS
from d_manager.nutrient.basics import Energy, Protein, Lipid, Carbohydrate, SaltEquivalent
from d_manager.helper.unit_helper import Unit
from d_manager.helper.prompt_helper import PromptHelper as Helper


class InteractiveProductFoodBookLoader:
    """対話的に市販食品を読み込む"""
    food_energy_unit = 'kcal'
    food_mass_unit = 'gram'

    @staticmethod
    def __get_group():
        """食品分類情報を取得する"""
        #
        # 日本食品標準成分表 2015 に収載されている食品群から選択
        Helper.print_msg('食品のグループを番号で選択してください。')
        group_id, group_name = Helper.choose_from_dict(GROUPS)
        return group_id, group_name

    @staticmethod
    def __get_product_labeling():
        """商品情報、特にパッケージにかかれている「一括表示」部分を取得する"""
        # 「一括表示」部分（商品名および名称など）の入力
        #
        # 参考
        #   加工食品品質表示基準改正（わかりやすい表示方法等）に関するQ&A｜消費者庁 - http://www.caa.go.jp/foods/qa/kakou04_qa.html#a09
        # 製造所の所在地及び製造者の氏名又は名称
        Helper.print_msg('製造者の氏名又は名称を入力してください。',
                         '備考: 包装内の一括表示内の「製造者」欄に記載されているもの。',
                         '     複数記載されている場合、は最初に記載されているものを採用すること。')
        maker_name = Helper.get_str()
        # 食品の名称と商品名は異なる。
        Helper.print_msg('食品の「商品名」を入力してください。', '注意: 一括表示内の「名称」のことではなく「商品名」です。')
        product_name = Helper.get_str()
        # また、名称の記載は義務だが、商品名の近くに記載してある場合は、一括表示欄に記載しなくてもよい。
        Helper.print_msg('食品の「名称」を入力してください。', '注意: 包装内の一括表示内の「名称」欄に記載されているものです。')
        food_name = Helper.get_str()

        return maker_name, product_name, food_name

    @staticmethod
    def __get_declaration_unit():
        """食品単位（「栄養成分表示」が表示する栄養素を含む食品の量）を取得する"""
        # 食品単位は、100g、100ml、１食分、１包装その他の１単位のいずれか（食品表示法）
        dimensionless = '1' + str(Unit.dimensionless)  # 次元がない単位
        declaration_units = ['100g', '100ml', dimensionless]

        Helper.print_msg('栄養成分表示の食品単位を入力してください。',
                         '食品単位は、栄養成分表示の基準となる量で 100g、100ml、もしくはその他の1単位で表記されています。',
                         '注意: 商品全体の内容量のことではないのに注意。')
        _, declaration_unit = Helper.choose_from_list(declaration_units)

        # 栄養成分表示の食品単位の物理量
        if declaration_unit == dimensionless:
            # 食品単位が1単位（１杯、１食分、１包装など）のどれかの場合は、
            # その1単位の物理量を明示的に指定する必要がある。
            Helper.print_msg('食品の1単位（１杯、１食分、１包装など）の物理量を記入してください。',
                             ''
                             '量の単位を以下から選択してください。')
            units = ['kg', 'g', 'ml', 'l']
            _, unit = Helper.choose_from_list(units)
            Helper.print_msg('量の数値を記入してください。')
            _quantity = str(Helper.get_float())
            return ''.join((_quantity, unit))
        else:
            # 食品単位が物理量だった場合はそれをそのまま利用する
            return declaration_unit

    @staticmethod
    def __get_nutrients(declaration_unit):
        """栄養素の取得"""
        nutrients = list()

        # 栄養成分表示の食品単位ごとの値
        # 各栄養素の単位は以下のガイドラインを参考にした。
        # 「食品表示法に基づく栄養成分表示のためのガイドライン 第1版 平成27年3月」
        #  http://www.caa.go.jp/foods/pdf/150331_GL-nutrition.pdf
        Helper.print_msg('栄養成分表示の入力',
                         '食品単位ごとの値です。食品単位={}'.format(declaration_unit))
        # 熱量
        Helper.print_msg('カロリーを入力してください。単位={:~P}'.format(Energy.default_units()))
        nutrients.append(Energy(Helper.get_integer()))
        # タンパク質
        Helper.print_msg('タンパク質を入力してください。単位={:~P}'.format(Protein.default_units()))
        nutrients.append(Protein(Helper.get_float()))
        # 脂質
        Helper.print_msg('脂質を入力してください。単位={:~P}'.format(Lipid.default_units()))
        nutrients.append(Lipid(Helper.get_float()))
        # 炭水化物
        Helper.print_msg('炭水化物を入力してください。単位={:~P}'.format(Carbohydrate.default_units()))
        nutrients.append(Carbohydrate(Helper.get_float()))
        # 食塩相当量
        Helper.print_msg('食塩相当量を入力してください。単位={:~P}'.format(SaltEquivalent.default_units()))
        nutrients.append(SaltEquivalent(Helper.get_float()))

        return nutrients

    @staticmethod
    def __confirm_and_add_food(group_id, food, book):
        group_name = GROUPS[group_id]
        Helper.print_msg('以下をグループ「{}」登録しますが、よろしいですか？'.format(group_name))
        Helper.print_product_food(food)
        if Helper.confirm_yes_of_no():
            _id = book.append(food, group_id)
            print('ID:{} として登録されました。'.format(_id))
        else:
            print('登録がキャンセルされました。')

    def load(self, book):
        """対話的に食品を読み込む"""
        while True:
            group_id, _ = self.__get_group()
            maker_name, product_name, food_name = self.__get_product_labeling()
            declaration_unit = self.__get_declaration_unit()
            nutrients = self.__get_nutrients(declaration_unit)
            product_food = ProductFood(maker_name=maker_name,
                                       product_name=product_name,
                                       food_name=food_name,
                                       amount=declaration_unit)
            product_food.nutrients = nutrients
            # 登録
            self.__confirm_and_add_food(group_id, product_food, book)

            Helper.print_msg('引き続き登録しますか？')
            if not Helper.confirm_yes_of_no():
                break
