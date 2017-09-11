#!/bin/sh
# 日本食品標準成分表2015年版（七訂）のエクセルファイルを一つ読み込んで一つの Pickle ファイルを作る。
base_dir=$(cd $(dirname "$0"); pwd)

CMD=${base_dir}/d-manager
PICKLE=${base_dir}/stofc2015r7_one.pickle

# test ディレクトリに以下のファイルをダウンロードして配置しておく。
# 全部入り
xlsx='1365334_1r10.xlsx'

convert_to_pickle_stofc2015r7(){
    $CMD convert_to_pickle stofc2015r7 -i "$1" > "$PICKLE"
}

set -ue
convert_to_pickle_stofc2015r7 "${base_dir}/${xlsx}"
