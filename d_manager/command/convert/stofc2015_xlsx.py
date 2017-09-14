import time
import argparse
import openpyxl

from d_manager.command import BaseCommand
from d_manager.nutrient.basics import Energy, Protein, Lipid, Carbohydrate, SaltEquivalent
from d_manager.food.stofc2015_food import STOFC2015Food
from d_manager.book.stofc2015_food_book import STOFC2015FoodBook
from d_manager.book.stofc2015_food_book import GROUPS
from d_manager.io.book_writer.pickle_book_writer import PickleBookWriter

# EXCEL ファイル内での各情報が格納されているセルの列番号
GROUP_ID_INDEX = 0
FOOD_ID_INDEX = 1
ID_IN_GROUP_INDEX = 2
FOOD_DESCRIPTION_INDEX = 3
ENERGY_INDEX = 5
PROTEIN_INDEX = 8
LIPID_INDEX = 10
CARBOHYDRATE_INDEX = 16
SALT_INDEX = 56
# SODIUM_INDEX = 22

# 日本食品標準成分表2015年版（七訂）では可食部 100 g当たりの成分表示となってるため、
# 各成分の単位は 100 gあたりに含まれる比率としている。
FOOD_AMOUNT = '100g'

# 各成分の単位
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


class ConvertSTOFC2015ExcelFileCommand(BaseCommand):
    """日本食品標準成分表2015年版の Excel ファイルを Pickle ファイルに変換するコマンド"""
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='対話的に市販食品を追加する。')
        parser.add_argument("-i", "--input", type=str,
                            required=True,
                            help="変換する Excel ファイル")
        parser.add_argument("-o", "--output", type=str,
                            required=False,
                            help="出力する Pickle ファイル")
        self.__args = parser.parse_args(args)
        self.__source_xlsx = self.__args.input
        self.__output_pickle = self.__args.output

    @staticmethod
    def __parse_food_value(_v):
        """食品の値をパースする"""
        # 以下の値を 0 と見做す
        _zero = ('Tr', '-', '(0)')
        if _v in _zero:
            return 0
        else:
            return float(_v)
    
    @staticmethod
    def __get_sub_groups_and_tags(grp, desc):
        """食品の分類情報と食品名から、サブグループとタグを取得する"""
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

    @classmethod
    def __get_food_from_row(cls, row):
        """行から食品データを作る"""
        # 食品群の名称（e.g. 調加工食品類）はグループの値から取得する。
        # 全ての食品群をまとめた Excel ファイルからインポートする場合は、シートのタイトルから食品群を取得することが出来ないため。
        group_name = GROUPS[int(row[GROUP_ID_INDEX].value)]
        food_description = row[FOOD_DESCRIPTION_INDEX].value
        # 食品の記述に食品群の分類情報が含まれている場合があるのでパースする。
        sub_groups, tags = cls.__get_sub_groups_and_tags(group_name, food_description)

        food = STOFC2015Food(sub_groups, tags, FOOD_AMOUNT)
        # 各種栄養素を生成する
        food.nutrient = Energy(cls.__parse_food_value(row[ENERGY_INDEX].value))
        food.nutrient = Protein(cls.__parse_food_value(row[PROTEIN_INDEX].value))
        food.nutrient = Lipid(cls.__parse_food_value(row[LIPID_INDEX].value))
        food.nutrient = Carbohydrate(cls.__parse_food_value(row[CARBOHYDRATE_INDEX].value))
        food.nutrient = SaltEquivalent(cls.__parse_food_value(row[SALT_INDEX].value))

        return food

    def do(self):
        # 現在は追記処理を作っていない。
        # 全ての食品群をまとめた Excel ファイルが配布されているので、
        # それをコンバートすれば用が足りるからである。
        food_book = STOFC2015FoodBook()

        # 統計情報
        start_time = time.time()
        num_of_process = dict()  # 食品群ごとの変換数
        for group_id in GROUPS.keys():
            num_of_process[group_id] = 0

        # Excel 読み込みとパース
        sheets = openpyxl.load_workbook(self.__source_xlsx, read_only=True)
        for sheet in sheets:
            for row in sheet.rows:
                # 有効な食品情報の含まれる行だけを抽出する
                if row[0].value is not None and row[0].value.isdigit():
                    food = self.__get_food_from_row(row)
                    food_id = int(row[FOOD_ID_INDEX].value)
                    food_book.append(food_id, food)

                    # 統計情報
                    group_id = int(row[GROUP_ID_INDEX].value)
                    num_of_process[group_id] += 1

            # 最初のシートのみを読み込む
            # 一括でまとまっている Excel ファイルには「別表」シートが付属しており、これはパースできない。
            break

        # 統計情報の表示
        all_of_num = 0
        for group_id, count in num_of_process.items():
            print('食品群 {}: {} 件処理しました。'.format(GROUPS[group_id], count))
            all_of_num += count
        else:
            print('合計: {} 件処理しました。({} sec)'.format(all_of_num, round(time.time() - start_time, 3)))

        # 追記モード（'ab'）でファイルを開いて書き込むと、
        # 追記前のデータが残るため取り出したときに追加したエントリが取り出せないので注意。
        writer = PickleBookWriter(self.__output_pickle, mode='wb')
        writer.write(food_book)
