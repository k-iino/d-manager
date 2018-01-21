#!/usr/bin/env python
# fixme
# 食事の記録は1日毎に記録する。
#
# ディレクトリ構造
# ${DMNGR_ROOT}
import sys
import os
import subprocess
import datetime
import argparse
import json
from json.decoder import JSONDecodeError

# 環境変数
ENV_MEALS_DIR = 'D_MANAGER_MEALS'
# fixme
# ENV_SUMMARIES_DIR = 'D_MANAGER_SUMMARIES'

# 許容する時刻の文字列形式
DATETIME_FORMAT = ('{}{}', '{} {}')
DATE_FORMATS = ('%Y%m%d', '%Y-%m-%d', '%Y/%m/%d')  # 年月日は省略不可能
TIME_FORMATS = ('', '%H%M', '%H:%M',
                '%H%M%S', '%H:%M:%S')

# 食事記録のパス
# ファイルとディレクトリの名前は年月日を元に決めている
MEAL_DIR_NAME_FORMAT = '%Y'
MEAL_FILE_NAME_FORMAT = '%m-%d'
MEAL_FILE_EXT = '.json'
# 食事記録内の時刻フォーマット
MEAL_TIME_FORMAT = '%H:%M:%S'

# 集計のパス
# ファイルとディレクトリの名前は年月日を元に決めている
# fixme
# SUMMARY_DIR_FORMAT = '%Y'
# SUMMARY_FILE_FORMAT = '%m-%d'
# SUMMARY_FILE_EXT = '.json'


def d_manager_meal(json_file=None):
    """d-manager meal コマンドの実行"""
    if json_file is not None:
        p = subprocess.run(['d-manager', 'meal', json_file], stdout=subprocess.PIPE)
    else:
        # ファイルの指定がなければ標準入力から受け取る
        json_str = ""
        for l in sys.stdin:
            json_str += l
        p = subprocess.run(['echo', json_str], stdout=subprocess.PIPE)
        p = subprocess.run(['d-manager', 'meal'], input=p.stdout, stdout=subprocess.PIPE)

    result = p.stdout.decode('utf-8')
    if result is not None:
        # todo
        # JSON にパース出来るかでコマンドが成功しているかを確認しているが、
        # コマンドの成功、失敗を別な方法で確認できれば、不要である
        json.loads(result)
        return result
    else:
        raise ValueError('結果が空')


def d_manager_summary(json_str):
    """d-manager summary コマンドの実行"""
    p = subprocess.run(['echo', json_str], stdout=subprocess.PIPE)
    p = subprocess.run(['d-manager', 'summary'], input=p.stdout, stdout=subprocess.PIPE)
    result = p.stdout.decode('utf-8')
    if result is not None:
        # todo
        # JSON にパース出来るかでコマンドが成功しているかを確認しているが、
        # コマンドの成功、失敗を別な方法で確認できれば、不要である
        try:
            json.loads(result)
        except JSONDecodeError as jde:
            print('error: {}'.format(result))
            raise jde
        return result
    else:
        raise ValueError('結果が空')


def get_datetime(date_str):
    """文字列から時刻を取得する"""
    date_str = date_str.lower()
    if date_str == 'now':
        dt = datetime.datetime.now()
    elif date_str == 'today':
        # now や詳細指定との差別化のため、日付のみの指定は時間は0時0分0秒とする。
        _dt = datetime.datetime.today()
        dt = datetime.datetime(year=_dt.year, month=_dt.month, day=_dt.day)
    elif date_str == 'yesterday':
        _dt = datetime.datetime.today() - datetime.timedelta(days=1)
        dt = datetime.datetime(year=_dt.year, month=_dt.month, day=_dt.day)
    elif date_str == 'tomorrow':
        _dt = datetime.datetime.today() + datetime.timedelta(days=1)
        dt = datetime.datetime(year=_dt.year, month=_dt.month, day=_dt.day)
    else:
        # 許容された日付のフォーマットで文字列を日付に変換する
        dt = None
        valid_dt_formats = (fmt.format(date, time) for fmt in DATETIME_FORMAT
                            for time in TIME_FORMATS
                            for date in DATE_FORMATS)
        for fmt in valid_dt_formats:
            try:
                fmt = fmt.strip()
                dt = datetime.datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue

        if dt is None:
            msg = '{} は適切な日付の文字列ではありません。'.format(date_str)
            raise ValueError(msg)

    return dt


def get_meal_dir_path(dt, base_dir='.'):
    """時刻から食事記録を格納するディレクトリのパスを得る"""
    return os.path.join(base_dir, dt.strftime(MEAL_DIR_NAME_FORMAT))


def get_meal_file_name(dt):
    """時刻から食事記録ファイルの名前を得る"""
    return dt.strftime(MEAL_FILE_NAME_FORMAT) + MEAL_FILE_EXT


def get_meal_file_full_path(meal_datetime, create_dir=False):
    """
    食事記録ファイルのパスを日付から取得

    :param meal_datetime:
    :param create_dir:
    :return: 食事記録ファイルのパス
    """
    # ディレクトリ準備
    # 日付から食事記録を格納するディレクトリパスを決定
    meal_dir = get_meal_dir_path(meal_datetime,
                                 base_dir=os.environ[ENV_MEALS_DIR])
    if not os.path.exists(meal_dir) and create_dir:
        os.makedirs(meal_dir)

    # ファイルのパスを作成
    meal_file_name = get_meal_file_name(meal_datetime)
    meal_path = os.path.join(meal_dir, meal_file_name)
    return meal_path


def append_meal(meal_file, meal_time, meal_json):
    """
    指定のファイルに、食事記録の JSON を追加する

    :param meal_file: 食事を追記するファイル
    :param meal_time: 食事を時刻
    :param meal_json: 追記する食事記録の JSON 文字列
    :return: 追加した食事記録ファイルの内容
    """
    meal_in_day = dict()
    # 既にファイルが存在する場合は、食事追加のために内容を予め読み込む
    if os.path.exists(meal_file):
        with open(meal_file, mode='r') as mf:
            meal_in_day = json.load(mf)

    new_meal = json.loads(meal_json)
    meal_time_str = meal_time.strftime(MEAL_TIME_FORMAT)
    if meal_time_str in meal_in_day.keys():
        # 同時刻の食事内容に追加する
        meal_in_day[meal_time_str] = new_meal + meal_in_day[meal_time_str]
    else:
        meal_in_day[meal_time_str] = new_meal

    meal_json = json.dumps(meal_in_day, ensure_ascii=False, indent=True)
    with open(meal_file, mode='w') as mf:
        mf.write(meal_json)

    return meal_json


def meal():
    """食事を日付に合わせたファイルに記録する"""
    parser = argparse.ArgumentParser(description='日付に合わせた食事記録ファイルを作成する')
    parser.add_argument('datetime',
                        metavar='DATETIME',
                        type=str,
                        nargs='?',
                        default='now',
                        help='日時')
    parser.add_argument('-j',
                        '--json',
                        metavar='JSON FILE',
                        type=str,
                        required=False,
                        default=None,
                        help='摂取した食事情報を記載した JSON ファイル')
    parsed_args = parser.parse_args()
    date_str = parsed_args.datetime.lower()
    json_file = parsed_args.json

    # d_manager meal コマンドを実行し、食品データベースから食事内容の詳細を取得
    new_meal_json = d_manager_meal(json_file)

    # 対応する日付ファイルに食事内容を追記
    meal_datetime = get_datetime(date_str)
    meal_file_path = get_meal_file_full_path(meal_datetime, create_dir=True)
    meal_json = append_meal(meal_file_path,
                            meal_datetime.time(),
                            new_meal_json)
    print(meal_json)


def adjust():
    """調整用の栄養成分を日付に合わせたファイルに記録する"""
    parser = argparse.ArgumentParser(description='日付に合わせた食事記録ファイルを作成する')
    parser.add_argument('datetime',
                        metavar='DATETIME',
                        type=str,
                        nargs='?',
                        default='now',
                        help='日時')
    parsed_args = parser.parse_args()
    datetime_str = parsed_args.datetime.lower()

    # 調整内容
    # 標準入力から受け取る
    json_str = ""
    for l in sys.stdin:
        json_str += l

    adjust_nutrients = json.loads(json_str)
    # 栄養素の配列が入力されることを前提とする
    energy = float(adjust_nutrients[0])
    protein = float(adjust_nutrients[1])
    lipid = float(adjust_nutrients[2])
    carbo = float(adjust_nutrients[3])
    salt = float(adjust_nutrients[4])

    # 調整用食事データのテンプレート
    adjust_meal_json = '''[
      {{
        "name": "adjust",
        "amount": "1 g",
        "nutrients": {{
          "energy": "{} kcal",
          "protein": "{} g",
          "lipid": "{} g",
          "carbohydrate": "{} g",
          "salt": "{} g"
        }}
      }}
    ]'''.format(energy, protein, lipid, carbo, salt)

    # 対応する日付ファイルに食事内容を追記
    adjust_datetime = get_datetime(datetime_str)
    meal_file_path = get_meal_file_full_path(adjust_datetime, create_dir=True)
    meal_json_in_day = append_meal(meal_file_path,
                                   adjust_datetime.time(),
                                   adjust_meal_json)
    print(meal_json_in_day)


def summary(args=None, return_value=False):
    """対象の日付の食事に含まれる栄養成分の総計を取得する"""
    parser = argparse.ArgumentParser(description='対象の日付の食事に含まれる栄養成分の総計を取得する')
    parser.add_argument('datetime',
                        metavar='DATETIME',
                        type=str,
                        nargs='?',
                        default='today',
                        help='日時')
    if args:
        parsed_args = parser.parse_args(args)
    else:
        parsed_args = parser.parse_args()
    datetime_str = parsed_args.datetime.lower()

    # 対応する日付
    target_date = get_datetime(datetime_str)

    # ターゲットの日付の食事記録を取得
    meal_file_path = get_meal_file_full_path(target_date, create_dir=True)
    with open(meal_file_path, mode='r') as mf:
        meal_in_day = json.load(mf)

    # 取得した日付の食事記録を１つのリストにまとめる
    meals_for_summary = list()
    for _, _meal in meal_in_day.items():
        meals_for_summary += _meal

    # d-manager summary でまとめた食事内容の内容を集計する
    summary_json = d_manager_summary(json.dumps(meals_for_summary, indent=True))
    if return_value:
        return summary_json
    else:
        print(summary_json)


def summary_all():
    """過去の食事記録をまとめて出力する"""
    parser = argparse.ArgumentParser(description='対象の日付の食事に含まれる栄養成分の総計を取得する')
    parser.add_argument('start',
                        metavar='START',
                        type=str,
                        help='出力する開始日')
    parser.add_argument('end',
                        metavar='END',
                        type=str,
                        help='出力する終了日')
    parser.add_argument('output_type',
                        metavar='OUTPUT_TYPE',
                        type=str,
                        nargs='?',
                        default='csv',
                        help='出力タイプ')
    parsed_args = parser.parse_args()
    output_type = parsed_args.output_type

    # 出力期間の開始日と終了日
    start_date = get_datetime(parsed_args.start).date()
    end_date = get_datetime(parsed_args.end).date()
    if not end_date >= start_date:
        msg = '終了日は開始日以降の日付である必要があります。開始日: {}, 終了日: {}'.format(start_date, end_date)
        raise ValueError(msg)

    output_data = dict()
    one_day = datetime.timedelta(days=1)
    while end_date >= start_date:
        _args = [str(start_date), ]
        try:
            _json_str = summary(_args, return_value=True)
            _summary = json.loads(_json_str)
            output_data[start_date] = _summary
        except FileNotFoundError:
            pass

        start_date += one_day

    if not len(output_data) > 0:
        msg = '対象期間内に食事データは存在しません。開始日: {}, 終了日: {}'.format(start_date, end_date)
        raise ValueError(msg)

    if output_type.lower() == 'csv':
        print('date, energy [kcal], protein [g], lipid [g], carbohydrate [g], salt [g]')
        for d, s in output_data.items():
            line = '{}, {}, {}, {}, {}, {}'.format(str(d),
                                                   s['energy'].rstrip('kcal').strip(),
                                                   s['protein'].rstrip('g').strip(),
                                                   s['lipid'].rstrip('g').strip(),
                                                   s['carbohydrate'].rstrip('g').strip(),
                                                   s['salt'].rstrip('g').strip())
            print(line)
    else:
        raise NotImplementedError(output_type)


def ratio():
    """Summary の結果から PFC 比率を出力する"""
    # 標準入力から受け取る
    json_str = ""
    for l in sys.stdin:
        json_str += l

    summary_data = json.loads(json_str)

    protein = float(summary_data['protein'].rstrip('g').strip())
    lipid = float(summary_data['lipid'].rstrip('g').strip())
    carbo = float(summary_data['carbohydrate'].rstrip('g').strip())
    sum = protein + lipid + carbo

    def _ratio(v):
        return int((v / sum) * 100)

    pfc_ratio = dict()
    pfc_ratio['pfc_ratio'] = '{}:{}:{}'.format(_ratio(protein),
                                               _ratio(lipid),
                                               _ratio(carbo),)
    print(json.dumps(pfc_ratio))


CMD_DISPATCH_TABLE = {'dmngr-meal': meal,
                      'dmngr-summary': summary,
                      'dmngr-summary-all': summary_all,
                      'dmngr-adjust': adjust,
                      'dmngr-ratio': ratio,
                      }

if __name__ == '__main__':
    cmd = os.path.basename(sys.argv[0])
    f = CMD_DISPATCH_TABLE[cmd]
    f()
