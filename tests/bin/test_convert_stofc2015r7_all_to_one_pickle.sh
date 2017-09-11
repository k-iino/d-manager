#!/bin/sh
# 日本食品標準成分表2015年版（七訂）の各エクセルファイルを
# 順に読み込んで一つの Pickle ファイルを作る。
# 実際は全部入りのファイルを使って作ったほうが楽である。
base_dir=$(cd $(dirname "$0"); pwd)

CMD=${base_dir}/d-manager
PICKLE=${base_dir}/stofc2015r7_all.pickle

# test ディレクトリに以下のファイルをダウンロードして配置しておく。
# 最初に読み込むファイル
first='1365344_1-0201r3.xlsx'
# 追加するエクセルファイル
sources='1365344_1-0202r.xlsx
1365344_1-0203r8.xlsx
1365344_1-0204r9.xlsx
1365344_1-0205r2.xlsx
1365344_1-0206r8.xlsx
1365344_1-0207r.xlsx
1365344_1-0208r.xlsx
1365344_1-0209.xlsx
1365344_1-0210r4.xlsx
1365344_1-0211r8.xlsx
1365344_1-0212r9.xlsx
1365344_1-0213r9.xlsx
1365344_1-0214r9.xlsx
1365344_1-0215r2.xlsx
1365344_1-0216r9.xlsx
1365344_1-0217r10.xlsx
1365344_1-0218.xlsx'


convert_to_pickle_stofc2015r7_first(){
    $CMD convert_to_pickle stofc2015r7 -i "$1" > "$PICKLE"
}

convert_to_pickle_stofc2015r7_append(){
    $CMD convert_to_pickle stofc2015r7 -i "$1" -a "$PICKLE"
}

convert_to_pickle_stofc2015r7_first "${base_dir}/${first}"
for s in $sources; do
    convert_to_pickle_stofc2015r7_append "${base_dir}/${s}"
done

