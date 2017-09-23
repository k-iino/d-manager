#!/usr/bin/env python
# d-manager のラッパー・プログラム
# 作成した食事記録を指定された日付に対応するディレクトリ内に作成する
#
# 使い方の例 1（標準入力から JSON を渡す）
# $ echo '[["stofc2015", 13023, 0.4]]' | dmngr-meal.py ['<日付>']
#
# 使い方の例 2（JSON ファイル）
# $ dmngr-meal.py [-j '<JSON ファイル>'] ['<日付>']
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='日付に合わせた食事記録ファイルを作成する')
    parser.add_argument('date', metavar='DATE', type=str,
                        nargs='?',
                        default='now',
                        help='日付')
    parser.add_argument('-j', '--json', metavar='JSON FILE', type=str,
                        required=False,
                        default=None,
                        help='摂取した食事情報を記載した JSON ファイル')
    parsed_args = parser.parse_args()
    date_str = parsed_args.date.lower()
    json_file = parsed_args.json

    # 環境変数から食事記録を保存するディレクトリのルートを取得
    meals_root = os.environ[ENV_MEALS_DIR]

    # 日付からファイルパスを決定
    # ファイル名が重複していた場合は、1 秒加算して作成
    dt = get_date(date_str)
    c = 0
    while True:
        td = datetime.timedelta(seconds=c)
        _dt = dt + td
        d, f = get_meal_file_path(_dt, base_dir=meals_root)
        # ディレクトリが存在しなかったらディレクトリ作成
        if not os.path.exists(d):
            os.makedirs(d)
        # ファイルが存在していないのならば問題ない
        meal_path = os.path.join(d, f)
        if not os.path.exists(meal_path):
            break
        else:
            c += 1

    # コマンドの実行
    if json_file is not None:
        p = subprocess.run(['d-manager', 'meal', json_file], stdout=subprocess.PIPE)
    else:
        # ファイルの指定がなければ標準入力から受け取る
        json_str = ""
        for l in sys.stdin:
            json_str += l
        p = subprocess.run(['echo', json_str], stdout=subprocess.PIPE)
        p = subprocess.run(['d-manager', 'meal'], input=p.stdout, stdout=subprocess.PIPE)

    # 出力
    result = p.stdout.decode('utf-8')
    with open(meal_path, mode='w') as f:
        f.write(result)

    print(result)
