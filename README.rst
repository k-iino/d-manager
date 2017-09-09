d-manager: Dietary manager
##########################

食品情報や食事を記録し管理をする Tool 群。

主機能
======

「食品表示法」で定められた栄養成分表示に準拠したフォーマットで食品や食事を記録する。
管理可能な食品は以下の通り。

* 文部科学省が公開している「日本食品標準成分表2015年版（七訂）」
  
  * Excel ファイルを Pickle, YAML ファイルに変換

* 市販食品（加工食品、生鮮食品）
      
  * 対話的に Pickle データに追加

動作環境
========

以下の環境で動作確認済み。

* Debian GNU/Linux 8 (jessie)
* Python 3.6.1

必要な外部パッケージは `requirements.txt` を参考のこと。

インストール
============

`bin/d-manager` へのシンボリックリンクをパスの通ったディレクトリに張る。

食品管理機能
=============

「日本食品標準成分表2015年版（七訂）」の管理
--------------------------------------------

基本操作
**********

日本食品標準成分表2015年版（七訂）の Excel ファイルは以下から入手可能。

`第2章　日本食品標準成分表　Exceｌ（日本語版）：文部科学省 <http://www.mext.go.jp/a_menu/syokuhinseibun/1365420.htm>`_

日本食品標準成分表2015年版（七訂）の Excel ファイルを Pickle ファイルに変換。

以下の例では、「1　穀類」の Excel ファイル（1365344_1-0201r3.xlsx）を Pickle ファイルに変換している。

.. code-block:: shell

   $ d-manager convert_to_pickle stofc2015r7 --input 1365344_1-0201r3.xlsx > output.pickle

日本食品標準成分表2015年版（七訂）の Excel ファイルを既にある Pickle ファイルに変換する。

以下の例では、「10　魚介類」の Excel ファイル（1365344_1-0210r4.xlsx）を Pickle ファイルに追加している。

.. code-block:: shell

   $ d-manager convert_to_pickle stofc2015r7 --input 1365344_1-0210r4.xlsx --append output.pickle

変換済みの日本食品標準成分表2015年版（七訂）の Pickle ファイルを YAML ファイルとして表示する。


.. code-block:: shell

   $ d-manager view_pickle_as_yaml stofc2015r7 --input output.pickle
   ...
   - classification:
       group: [いも及びでん粉類, でん粉・でん粉製品, でん粉製品]
       tag_name: [はるさめ, 普通はるさめ, 乾]
     food:
       amount: 100 g
       name: はるさめ, 普通はるさめ, 乾
       nutrient: {carbohydrate: 86.6 g, energy: 350 kcal, lipid: 0.2 g, protein: 0 g,
         salt_equivalent: 0 g}
     id: 2040
   - classification:
       group: [いも及びでん粉類, でん粉・でん粉製品, でん粉製品]
       tag_name: [はるさめ, 普通はるさめ, ゆで]
     food:
       amount: 100 g
       name: はるさめ, 普通はるさめ, ゆで
       nutrient: {carbohydrate: 19.9 g, energy: 80 kcal, lipid: 0 g, protein: 0 g, salt_equivalent: 0
           g}
     id: 2062

一括変換
*********

`bin/convert_stofc2015r7_to_one_pickle.sh` というスクリプトを利用することで、一括して日本食品標準成分表2015年版（七訂）の Excel ファイルを `stofc2015r7_all.pickle` という Pickle ファイルに変換可能。

このスクリプトと同階層に現在（2017年9月）公開されている日本食品標準成分表2015年版（七訂）の Excel ファイル全て（「1　穀類」から「18　調理加工食品類」）を配置してから、このスクリプトを実行する。

.. code-block:: shell

   $ ls
   1365344_1-0201r3.xlsx  1365344_1-0204r9.xlsx  1365344_1-0207r.xlsx  1365344_1-0210r4.xlsx  1365344_1-0213r9.xlsx
   1365344_1-0216r9.xlsx   convert_stofc2015r7_to_one_pickle.sh
   1365344_1-0202r.xlsx   1365344_1-0205r2.xlsx  1365344_1-0208r.xlsx  1365344_1-0211r8.xlsx  1365344_1-0214r9.xlsx
   1365344_1-0217r10.xlsx  d-manager 1365344_1-0203r8.xlsx  1365344_1-0206r8.xlsx  1365344_1-0209.xlsx
   1365344_1-0212r9.xlsx  1365344_1-0215r2.xlsx  1365344_1-0218.xlsx
   $ ./convert_stofc2015r7_to_one_pickle.sh
   append: ./d-manager/bin/1365344_1-0202r.xlsx  to  ./d-manager/bin/stofc2015r7_all.pickle
   ...
   append: ./d-manager/bin/1365344_1-0218.xlsx  to  ./d-manager/bin/stofc2015r7_all.pickle
   $ ls -1 | grep all.pickle
   stofc2015r7_all.pickle

食品群の名前を Excel ファイルのシート名から取得しているが、現在（2017年9月）公開されている日本食品標準成分表2015年版（七訂）の「18　調理加工食品類」ファイルは（1365344_1-0218.xlsx）はシート名が「18　調加工食品類」とタイプミスしている。
そのため、取り込む前にシート名を「18　調理加工食品類」と修正しておくこと。