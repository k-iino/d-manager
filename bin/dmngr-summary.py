#!/usr/bin/env python
# d-manager のラッパー・プログラム
# 食事記録を元に日付毎の要約ファイルを作成する。
#
# $ dmngr-summary.py [-v|--verbose]
#
# [-v|--verbose] オプションをつけると、要約したファイルを標準出力に表示する。
#
# 要約情報は、環境変数 D_MANAGER_SUMMARIES をルートとするディレクトリ以下に配置する。
# 要約情報ファイルのパスは日付によって分類、配置される。
# 配置の規則は helper/date.py を参照のこと。
#
# 食事情報は、予め、 dmngr-meal.py コマンドで適切なディレクトリに配置されているものとする。
# 詳しい配置規則は dmngr-meal.py を参照のこと。
#
import os
import subprocess
import datetime
import argparse

from helper.date import get_summary_file_path
from helper.date import get_date_from_meal_file

# 環境変数
ENV_MEALS_DIR = 'D_MANAGER_MEALS'
ENV_SUMMARIES_DIR = 'D_MANAGER_SUMMARIES'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='食事記録の要約ファイルを生成する')
    parser.add_argument('-v', '--verbose', action='store_true',
                        required=False,
                        default=False,
                        help='摂取した食事情報を記載した JSON ファイル')
    parsed_args = parser.parse_args()

    # 環境変数から各種保存ディレクトリのルートを取得
    meals_root = os.environ[ENV_MEALS_DIR]
    summaries_root = os.environ[ENV_SUMMARIES_DIR]

    # 食事記録を辿り、日付ごとに食事記録の JSON ファイルをまとめる
    meal_json = dict()
    key_fmt = '%Y%m%d'
    for path, dirs, files in os.walk(meals_root):
        for file in files:
            # JSON ファイルだけが対象
            # todo 調整用食事がこの実装だと漏れるかもしれない
            if file.endswith('.json'):
                # 食事記録ファイルの日付を得る
                date_str = get_date_from_meal_file(path, file).strftime(key_fmt)
                if date_str not in meal_json.keys():
                    meal_json[date_str] = list()
                # JSON ファイルのパスを格納
                meal_json[date_str].append(os.path.join(path, file))

    # 集計された日付ごとの食事記録を元に要約を作成していく
    for dt_str, json_files in meal_json.items():
        dt = datetime.datetime.strptime(dt_str, key_fmt)
        # JSON ファイルをまとめて引数へ
        cmd = ['d-manager', 'summary'] + list(json_files)
        # 要約コマンドの実行
        p = subprocess.run(cmd, stdout=subprocess.PIPE)
        result = p.stdout.decode('utf-8')
        # 要約情報を保存するためのディレクトリを取得
        dt = datetime.datetime.strptime(dt_str, key_fmt)
        _dir, _file = get_summary_file_path(dt, base_dir=summaries_root)
        # ディレクトリが存在しなかったらディレクトリ作成
        if not os.path.exists(_dir):
            os.makedirs(_dir)

        # 内容を書き込み（上書き）
        file_path = os.path.join(_dir, _file)
        with open(file_path, mode="w") as f:
            f.write(result)

        # 表示
        if parsed_args.verbose:
            print(file_path)
