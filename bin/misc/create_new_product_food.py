#!/usr/bin/env python
# 市販の一般加工食品用の食品データをテンプレートから作成する
# グループ内での ID 重複や食品ファイルの上書きを防ぐ
import os
import argparse
import math

# ファイル名のフォーマット
FILE_EXT = '.json'
ID_IN_GROUP_DIGITS = 3  # グループ内の ID の桁
FILE_NAME_FORMAT = '{:d}{:0' + str(ID_IN_GROUP_DIGITS) + 'd}'

# 作成可能な食品グループ
FOOD_GROUPS = {
    1: '穀類',
    2: 'いも及びでん粉類',
    3: '砂糖及び甘味類',
    4: '豆類',
    5: '種実類',
    6: '野菜類',
    7: '果実類',
    8: 'きのこ類',
    9: '藻類',
    10: '魚介類',
    11: '肉類',
    12: '卵類',
    13: '乳類',
    14: '油脂類',
    15: '菓子類',
    16: 'し好飲料類',
    17: '調味料及び香辛料類',
    18: '調理加工食品類',
}

JSON_TEMPLATE = '''{
  "name": "",
  "amount": " g",
  "maker": "",
  "product name": "",
  "nutrients": {
    "energy": " kcal",
    "protein": " g",
    "lipid": " g",
    "carbohydrate": " g",
    "salt": " g"
  }
}
'''


def print_groups():
    """食品グループを表示する"""
    print('選択可能な食品グループ')
    for k, n in FOOD_GROUPS.items():
        print('{}: {}'.format(k, n))


def get_group_id(_id):
    """ID から食品のグループの ID とグループ内 ID を取得する"""
    _id = int(_id)
    _group_id = math.floor(_id / (10 ** ID_IN_GROUP_DIGITS))
    _id_in_group = _id - (_group_id * (10 ** ID_IN_GROUP_DIGITS))
    return _group_id, _id_in_group


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='日付に合わせた食事記録ファイルを作成する')
    parser.add_argument('group', metavar='GROUP', type=int,
                        help='食品群')
    # parser.add_argument('-j', '--json', metavar='JSON FILE', type=str,
    #                     required=False,
    #                     default=None,
    #                     help='テンプレート JSON ファイル')
    parsed_args = parser.parse_args()
    group_id = parsed_args.group

    if group_id not in FOOD_GROUPS.keys():
        print('{} は選択不可能な食品群です。'.format(group_id))
        print_groups()

    # 同じグループの食品をリストアップ
    same_group_food_ids = list()
    for f in os.listdir(os.getcwd()):
        if f.endswith(FILE_EXT):
            _id = f.rstrip(FILE_EXT)
            if _id.isdigit():
                _id = int(_id)
                new_group_id, _id_in_group = get_group_id(_id)
                if group_id == new_group_id:
                    same_group_food_ids.append(_id)

    # グループ内で最大の ID を取得
    max_id = int(FILE_NAME_FORMAT.format(group_id, 0).strip())
    for _id in same_group_food_ids:
        if _id > max_id:
            max_id = _id

    # ID を生成
    # グループ内の最大 ID の次の整数
    new_id = max_id + 1
    # オーバーフロー確認
    # グループ番号が変わっていたらオーバーフローが発生したものとする
    new_group_id, new_id_in_group = get_group_id(new_id)
    if new_group_id != group_id:
        raise ValueError('グループ {} でオーバーフロー発生'.format(group_id))

    new_file = FILE_NAME_FORMAT.format(new_group_id, new_id_in_group)
    new_file = new_file.strip() + FILE_EXT
    # 存在確認
    if os.path.exists(new_file):
        # このエラーが発生したら、 ID 取得の実装が間違っている
        raise FileExistsError('{}'.format(new_file))

    # 作成
    with open(new_file, mode='w') as f:
        f.write(JSON_TEMPLATE)

    # パスを表示
    print(new_file)
