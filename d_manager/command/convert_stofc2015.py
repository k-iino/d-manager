import os
import argparse
import json
import openpyxl

# 日本食品標準成分表2015年版（七訂）Excel ファイルから各情報を取り出すための定数群
# 定数の構造は以下の通り
#
#   定数名 = (情報が含まれるセルの列番号, 成分のキー名, 成分の単位,)
#
# 各成分の単位については、日本食品標準成分表2015年版（七訂）第1章 説明 p.「表 14 数値の表示方法」を参考にすること
# 参考: http://www.mext.go.jp/a_menu/syokuhinseibun/1365297.htm
# GROUP_ID = (0, None, None)
FOOD_ID = (1, None, None)
# ID_IN_GROUP = (2, None, None)
FOOD_DESCRIPTION = (3, None, None)
ENERGY = (5, 'energy', 'kcal')
PROTEIN = (8, 'protein', 'g')
LIPID = (10, 'lipid', 'g')
CARBOHYDRATE = (16, 'carbohydrate', 'g')
SALT = (56, 'salt', 'g')

# 日本食品標準成分表2015年版（七訂）では可食部 100g 当たりの成分表示となってるため、
# 各食品の食品単位は 100g とする。
FOOD_AMOUNT = '100g'


def _parse_food_value(_v):
    """食品の値をパースする"""
    # 以下の値を 0 と見做す
    _zero = ('Tr', '-', '(0)')
    if _v in _zero:
        return 0
    else:
        return float(_v)


class ConvertStofc2015Command:
    """日本食品標準成分表2015年版の Excel ファイルを食品データファイル群に変換"""
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='日本食品標準成分表2015年版の Excel ファイルを食品データファイル群に変換する。')
        parser.add_argument("-x", "--xlsx", type=str,
                            required=True,
                            help="変換対象の Excel ファイル")
        parser.add_argument("-o", "--output_dir", type=str,
                            required=True,
                            help="出力する食品ファイルを配置するディレクトリ")
        parsed_args = parser.parse_args(args)
        self.source_xlsx = parsed_args.xlsx
        self.output_dir = parsed_args.output_dir

    def do(self):
        # 出力先の確保
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        os.chdir(self.output_dir)

        # Excel 読み込みとパース
        book = openpyxl.load_workbook(self.source_xlsx, read_only=True)

        # 最初のシートのみを処理対象とする
        # 一括版 Excel ファイルには「別表」シートが付属しており、これはパースしない
        target_sheet = book.worksheets[0]

        for row in target_sheet.rows:
            # 無効な食品情報の含まれる行は処理対象外
            if row[0].value is None or not row[0].value.isdigit():
                continue

            food_info = dict()
            food_info['name'] = row[FOOD_DESCRIPTION[0]].value.strip()
            food_info['amount'] = FOOD_AMOUNT

            # 栄養成分
            nutrients = dict()
            # 基本 5 項目
            basic5 = list()
            basic5.append((ENERGY[1], row[ENERGY[0]].value, ENERGY[2]))
            basic5.append((PROTEIN[1], row[PROTEIN[0]].value, PROTEIN[2]))
            basic5.append((LIPID[1], row[LIPID[0]].value, LIPID[2]))
            basic5.append((CARBOHYDRATE[1], row[CARBOHYDRATE[0]].value, CARBOHYDRATE[2]))
            basic5.append((SALT[1], row[SALT[0]].value, SALT[2]))
            for n in basic5:
                key = n[0]
                magnitude = _parse_food_value(n[1])
                unit = n[2]
                nutrients[key] = '{} {}'.format(magnitude, unit)

            food_info['nutrients'] = nutrients

            # JSON ファイル作成
            food_id = int(row[FOOD_ID[0]].value)
            file_name = '{:05d}.json'.format(food_id)
            file_path = os.path.join(self.output_dir, file_name)
            with open(file_path, mode='w') as f:
                json_str = json.dumps(food_info, ensure_ascii=False, indent=2)
                f.write(json_str)
