import sys
import pickle
import openpyxl
import yaml

from d_manager.data import Food
from d_manager.data.entry import ProductFoodEntry
from d_manager.data.entry import STOFC2015r7FoodEntry

from d_manager.book.helper import InteractiveHelper


class LoaderBase:
    def __init__(self):
        pass

    def load(self, entries):
        raise NotImplementedError


class FileLoaderBase(LoaderBase):
    """ファイルで読み込むベースローダ"""

    def __init__(self, file):
        self.file = file
        super(FileLoaderBase, self).__init__()

    def load(self, entries):
        raise NotImplementedError


class ExcelLoaderBase(LoaderBase):
    """エクセルファイルからロードする"""

    def __init__(self, xlsx):
        self.book = openpyxl.load_workbook(xlsx, read_only=True)
        super(ExcelLoaderBase, self).__init__()

    def load(self, entries):
        raise NotImplementedError


class STOFC2015r7FoodPickleLoader(FileLoaderBase):
    """Pickle ファイルから日本食品標準成分表2015年版（七訂）の食品を読み込むローダー"""
    def load(self, entries):
        if self.file == sys.stdin:
            entries.update(pickle.load(sys.stdin))
        else:
            with open(self.file, mode='rb') as f:
                for e in pickle.load(f).values():
                    if isinstance(e, STOFC2015r7FoodEntry):
                        entries[e.id] = e
                    else:
                        raise ValueError('不正な値です。 Pickle ファイルに予想とは異なる型のエントリが含まれています。')


class STOFC2015r7FoodExcelLoader(ExcelLoaderBase):
    """日本食品標準成分表2015年版（七訂）のエクセル用ローダー"""

    # EXCEL ファイル内での各情報が格納されているセルの列番号
    GROUP_ID_INDEX = 0
    ID_INDEX = 1
    TAG_NAME_INDEX = 3
    ENERGY_INDEX = 5
    PROTEIN_INDEX = 8
    LIPID_INDEX = 10
    CARBO_INDEX = 16
    SALT_INDEX = 56
    SODIUM_INDEX = 22

    # 各成分の単位
    #
    # 日本食品標準成分表2015年版（七訂）では可食部 100 g当たりの成分表示となってるため、
    # 各成分の単位は 100 gあたりに含まれる比率としている。
    # 単位については、日本食品標準成分表2015年版（七訂）第1章 説明 p.「表 14 数値の表示方法」を参考のこと
    #
    # 参考
    #   http://www.mext.go.jp/a_menu/syokuhinseibun/1365297.htm
    ENERGY_UNIT = 'kcal'
    PROTEIN_UNIT = 'g'
    LIPID_UNIT = 'g'
    CARBO_UNIT = 'g'
    SALT_UNIT = 'g'
    SODIUM_UNIT = 'mg'
    
    @staticmethod
    def __classify(grp, desc):
        """
        食品の分類情報と食品名を記述から抽出

        :param grp: 食品群名
        :param desc: 食品記述
        :return:
        """
        # 食品の分類を大きく２つの区分に分けている。
        #   1. 食品群（food_group）
        #   2. 分類情報（product_info）
        food_group = [grp]
        product_info = []

        # 日本食品標準成分表2015年版（七訂）では各食品群内での食品の分類は以下のようにしている。
        #
        #    "収載食品の分類は成分表2010と同じく大分類、中分類、小分類及び細分の四段階とした。
        #    食品の大分類は原則として動植物の名称をあて、五十音順に配列した。
        #    ただし、「いも及びでん粉類」、「魚介類」、「肉類」、「乳類」、「し好飲料類」
        #    及び「調味料及び香辛料類」は、大分類の前に副分類（＜ ＞で表示）を設けて食品群を区分した。
        #    また、食品によっては、大分類の前に類区分（（ ）で表示）を五十音順に設けた。
        #    中分類（［ ］で表示）及び小分類は、原則として原材料的形状から順次加工度の高まる順に配列した。
        #    ただし、原材料が複数からなる加工食品は、原則として主原材料の位置に配列した。"
        #   『日本食品標準成分表2015年版（七訂）』（第1章　説明）より
        #

        # 食品群の下位区分の追加
        # 分類情報の記述に食品群の下位区分が記載されているならば、それを抽出して食品群の情報に加える。
        def append_lower_group(_sep: tuple, _desc: str, _food_group: list):
            if _sep[0] in _desc:
                begin = _desc.find(_sep[0]) + 1
                end = _desc.find(_sep[1])
                _food_group.append(_desc[begin:end].strip())
                # 食品記述から下位区分を取り除いた文字列を返す
                return _desc[:begin - 1] + _desc[end + 1:]
            else:
                return _desc

        # 副分類
        desc = append_lower_group(('＜', '＞'), desc, food_group)
        # 類区分
        desc = append_lower_group(('（', '）'), desc, food_group)

        # 分類情報
        # 日本食品標準成分表では原材料的食品と加工食品が収載されているが、
        # 加工食品では大分類に動植物の名称があてられるという原則が守られていない。
        # そのため、各段階の分類は形式上のものと判断し、大分類から順にリスト構造のデータとして扱っている。
        for term in desc.split():
            if len(term):
                product_info.append(term.strip())

        return food_group, product_info

    def load(self, entries):
        def presume_value(_v):
            # 以下の値を 0 と見做す
            _zero = ('Tr', '-')
            # print(_v)
            if _v in _zero:
                return 0

            return _v

        cls_ = STOFC2015r7FoodExcelLoader
        for sheet in self.book:
            for row in sheet.rows:
                if len(row) <= 0:
                    continue

                # 有効な食品情報の含まれる行だけを抽出する
                if row[0].value is not None and row[0].value.isdigit():
                    # 食品群（e.g. 調加工食品類）の名称は食品群を表すセル内の値から取得する。
                    # 全ての食品群をまとめた Excel ファイルをインポートする場合は、シート名などから
                    # 食品群の文字列を取得することが出来ないため。
                    group_id = int(row[0].value)
                    group = STOFC2015r7FoodEntry.FOOD_GROUPS[group_id]
                    group_name, tag_name = self.__classify(group, row[cls_.TAG_NAME_INDEX].value)
                    # ID
                    _id = int(row[cls_.ID_INDEX].value)
                    food = Food(' '.join(tag_name), '100g')  # CSV 出力のことを考えて空白区切りと
                    food.energy = str(presume_value(row[cls_.ENERGY_INDEX].value)) + cls_.ENERGY_UNIT
                    food.protein = str(presume_value(row[cls_.PROTEIN_INDEX].value)) + cls_.PROTEIN_UNIT
                    food.lipid = str(presume_value(row[cls_.LIPID_INDEX].value)) + cls_.LIPID_UNIT
                    food.carbohydrate = str(presume_value(row[cls_.CARBO_INDEX].value)) + cls_.CARBO_UNIT
                    food.salt = str(presume_value(row[cls_.SALT_INDEX].value)) + cls_.SALT_UNIT

                    entries[_id] = STOFC2015r7FoodEntry(_id, group_name, tag_name, food)

            # 最初のシートのみを読み込む
            # 一括でまとまっている Excel ファイルは「別表」シートが付属しており、これはパースできない。
            break


class ProductFoodPickleLoader(FileLoaderBase):
    """ Pickle ファイル内の市販食品を読み込むローダー"""
    def load(self, entries):
        if self.file == sys.stdin:
            entries.update(pickle.load(sys.stdin))
        else:
            with open(self.file, mode='rb') as f:
                for e in pickle.load(f).values():
                    if isinstance(e, ProductFoodEntry):
                        entries[e.id] = e
                    else:
                        raise ValueError('不正な値です。 Pickle ファイルに予想とは異なる型のエントリが含まれています。')


class InteractivelyProductFoodLoader(LoaderBase):
    """対話的に市販食品を読み込む"""
    @staticmethod
    def __print_msg(*msgs, sep='\n'):
        print(sep.join(msgs))

    def load(self, entries):
        helper = InteractiveHelper
        # 食品分類
        #
        # 日本食品標準成分表 2015 に収載されている食品群から選択
        self.__print_msg('食品のグループを番号で選択してください。')
        group_number, group_name = helper.choose_from_dict(STOFC2015r7FoodEntry.FOOD_GROUPS)

        # 商品名および名称
        #
        # 食品の名称と商品名は異なる。
        # また、名称の記載は義務だが、商品名の近くに記載してある場合は、一括表示欄に記載しなくてもよい。
        #
        # 参考
        #   加工食品品質表示基準改正（わかりやすい表示方法等）に関するQ&A｜消費者庁 - http://www.caa.go.jp/foods/qa/kakou04_qa.html#a09
        self.__print_msg('食品の「商品名」を入力してください。', '注意: 一括表示内の「名称」のことではなく「商品名」です。')
        product_name = helper.get_str()
        self.__print_msg('食品の「名称」を入力してください。', '注意: 包装内の一括表示内の「名称」欄に記載されているものです。')
        common_name = helper.get_str()

        # 製造所の所在地及び製造者の氏名又は名称
        self.__print_msg('製造者の氏名又は名称を入力してください。',
                         '備考: 包装内の一括表示内の「製造者」欄に記載されているもの。',
                         '     複数記載されている場合、は最初に記載されているものを採用すること。')
        maker = helper.get_str()

        # 栄養成分表示
        #
        # 食品単位は、100g、100ml、１食分、１包装その他の１単位のいずれか（食品表示法）
        dimensionless_unit = 'dimensionless'
        nutrient_units = ['100g', '100ml', '1' + dimensionless_unit]
        self.__print_msg('栄養成分表示の食品単位を入力してください。',
                         '食品単位は、栄養成分表示の基準となる量で 100g、100ml、もしくはその他の1単位で表記されています。',
                         '注意: 商品の内容量ではないので注意。')
        _, nutrient_declaration_unit = helper.choose_from_list(nutrient_units)
        # 栄養成分表示の食品単位の物理量
        if nutrient_declaration_unit == '1' + dimensionless_unit:
            # 食品単位が1単位（１杯、１食分、１包装など）のどれかの場合は、
            # その1単位の物理量を明示的に指定する必要がある。
            self.__print_msg('食品の1単位（１杯、１食分、１包装など）の物理量を記入してください。',
                             '栄養成分表示の食品単位に併記されている物理量を記入してくだい。'
                             ''
                             '量の単位を以下から選択してください。')
            # 食品1単位（１杯、１食分、１包装など）の物理量の単位
            one_packet_units = ['kg', 'g', 'ml', 'l']
            _, _unit = helper.choose_from_list(one_packet_units)
            self.__print_msg('量の数値を記入してください。')
            _quantity = str(helper.get_float())
            food_amount = ''.join((_quantity, _unit))
        else:
            # 食品単位が物理量だった場合はそれをそのまま利用する
            food_amount = nutrient_declaration_unit

        # 各栄養素
        #
        # 栄養成分表示の食品単位ごとの値
        # 各栄養素の単位は以下のガイドラインを参考にした。
        # 「食品表示法に基づく栄養成分表示のためのガイドライン 第1版 平成27年3月」
        #  http://www.caa.go.jp/foods/pdf/150331_GL-nutrition.pdf
        food_energy_unit = 'kcal'
        food_mass_unit = 'gram'

        self.__print_msg('栄養成分表示の入力',
                         '食品単位ごとの値です。入力された食品単位={}'.format(nutrient_declaration_unit))
        # 熱量
        self.__print_msg('カロリーを入力してください。単位={}'.format(food_energy_unit))
        energy_quantity = str(helper.get_integer())
        # タンパク質
        self.__print_msg('タンパク質を入力してください。単位={}'.format(food_mass_unit))
        protein_quantity = str(helper.get_float())
        # 脂質
        self.__print_msg('脂質を入力してください。単位={}'.format(food_mass_unit))
        lipid_quantity = str(helper.get_float())
        # 炭水化物
        self.__print_msg('炭水化物を入力してください。単位={}'.format(food_mass_unit))
        carbohydrate_quantity = str(helper.get_float())
        # 食塩相当量
        self.__print_msg('食塩相当量を入力してください。単位={}'.format(food_mass_unit))
        salt_equivalent_quantity = str(helper.get_float())

        #
        # 食品情報の生成
        #

        # グループ内で一意な番号は自動で採番する
        # グループ内で最も大きな番号を持つものより 1 つ大きいものを採用する。
        max_id_in_group = 0
        for e in entries.values():
            if e.group_number == group_number and e.id_in_group > max_id_in_group:
                max_id_in_group = e.id_in_group
        else:
            id_in_group = max_id_in_group + 1

        food = Food(common_name, food_amount)
        # 栄養成分
        food.energy = ''.join((energy_quantity, food_energy_unit))
        food.protein = ''.join((protein_quantity, food_mass_unit))
        food.lipid = ''.join((lipid_quantity, food_mass_unit))
        food.carbohydrate = ''.join((carbohydrate_quantity, food_mass_unit))
        food.salt = ''.join((salt_equivalent_quantity, food_mass_unit))
        # 製品情報
        entry = ProductFoodEntry(group_number, id_in_group, product_name, maker, food)

        self.__print_msg('以下を登録しますが、よろしいですか？')
        print(yaml.dump(entry.to_dict(), allow_unicode=True))
        if helper.confirm_yes_of_no():
            entries[entry.id] = entry
            print('{} が登録されました。'.format(entry.id))
        else:
            print('追加登録がキャンセルされました。')
