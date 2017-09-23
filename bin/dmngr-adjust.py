#!/usr/bin/env python
# d-manager のラッパー・プログラム
# 指定された日付の調整用食事のファイルを生成する。
#
# 使い方の例 1（標準入力から JSON を渡す）
# $ dmngr-adjust.py ['<日付>']
#
# 指定可能な日付は 'now', 'today', 'yesterday', その他形式
# その他形式については、 helper/date.py を参照のこと。
# 日付を省略した場合は、'now' が選択されたものとする。
#
# 食事情報は、日付に対応するディレクトリ内に作成される。
# ディレクトリは環境変数 'D_MANAGER_MEALS' をルートとする。
#
import os
import sys
import subprocess
import datetime
import argparse

from helper.date import get_date
from helper.date import get_meal_file_path

# 環境変数
ENV_MEALS_DIR = 'D_MANAGER_MEALS'

# 調整用食事データのファイル名
# dmngr-summary.py コマンドは食事記録を集計するときに食事記録のファイル名が日時や時刻を表す文字列であることを期待している。
# そのため、それ以外のフォーマット（英字のみなど）のファイル名で調整用食事データを作成すると、そのファイルが集計されない。
# また、通常の食事記録と時刻で重複しないように、調整用食事データのファイル名は23時59分59秒の食事とする。
ADJUST_TIME = datetime.time(hour=23, minute=59, second=59)

# 調整用食事データのテンプレート
TEMPLATE = '''[
  {
    "name": "adjust",
    "amount": "0 g",
    "nutrients": {
      "energy": "0 kcal",
      "protein": "0 g",
      "lipid": "0 g",
      "carbohydrate": "0 g",
      "salt": "0 g"
    }
  }
]'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='日付に合わせた食事記録ファイルを作成する')
    parser.add_argument('date', metavar='DATE', type=str,
                        nargs='?',
                        default='now',
                        help='日付')
    # parser.add_argument('-j', '--json', metavar='JSON FILE', type=str,
    #                     required=False,
    #                     default=None,
    #                     help='テンプレート JSON ファイル')
    parsed_args = parser.parse_args()
    date_str = parsed_args.date.lower()
    # json_file = parsed_args.json

    # 環境変数から食事記録を保存するディレクトリのルートを取得
    meals_root = os.environ[ENV_MEALS_DIR]

    # 日付からファイルパスを決定
    _dt = get_date(date_str)
    # 通常の食事記録と時刻で重複しないように、調整用食事データのファイル名は設定された時刻のものとする
    dt = datetime.datetime(year=_dt.year, month=_dt.month, day=_dt.day,
                           hour=ADJUST_TIME.hour, minute=ADJUST_TIME.minute, second=ADJUST_TIME.second)
    # 調整用ファイルのパス
    d, f = get_meal_file_path(dt, base_dir=meals_root)
    # ディレクトリが存在しなかったらディレクトリ作成
    if not os.path.exists(d):
        os.makedirs(d)
    # ファイルが存在していたら処理を続けない
    adjust_meal_path = os.path.join(d, f)
    if os.path.exists(adjust_meal_path):
        raise FileExistsError(adjust_meal_path)

    # 出力
    with open(adjust_meal_path, mode='w') as f:
        f.write(TEMPLATE)

    # ファイルのパスを指定。
    print(adjust_meal_path)
