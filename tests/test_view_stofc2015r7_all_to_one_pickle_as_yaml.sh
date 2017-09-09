#!/bin/sh
# 日本食品標準成分表2015年版（七訂）の Pickle ファイルを YAML ファイルに変換するテスト。
# 先に test_convert_stofc2015r7_all_to_one_pickle.sh で読み込み対象のファイルを作っておく必要がある。
base_dir=$(cd $(dirname "$0"); pwd)

CMD="${base_dir}/d-manager"
PICKLE="${base_dir}/stofc2015r7_all.pickle"
YAML="${base_dir}/output.yaml"

view_pickle_stofc2015r7(){
    $CMD view_pickle_as_yaml stofc2015r7 -i "$1"
}

set -eu
view_pickle_stofc2015r7 "${PICKLE}" > "${YAML}"
cat ${YAML}
num=$(cat ${YAML}  | grep '  id: ' | wc -l)
echo "YAML に変換された食品数: $num"
echo "参考: 日本食品標準成分表2015年版（七訂）に掲載されている食品数は 2191"