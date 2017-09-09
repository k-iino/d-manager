##########################
d-manager: Dietary manager
##########################

食品情報や食事を記録し管理をするためのコマンド。

日々の食事を管理するための

***************
主機能
***************

「食品表示法」及び「食品表示基準」で定められた栄養成分表示に準拠したフォーマットで食品や食事を記録する。
管理可能な食品は以下の通り。

* 文部科学省が公開している「日本食品標準成分表2015年版（七訂）」
  
  * Excel ファイルを Pickle, YAML ファイルに変換

* 市販食品（加工食品、生鮮食品）
      
  * 対話的に Pickle データに追加

***************
動作環境
***************

以下の環境で動作確認済み。

* Debian GNU/Linux 8 (jessie)
* Python 3.6.1

必要な外部パッケージは `requirements.txt` を参考のこと。

***************
インストール
***************

`bin/d-manager` へのシンボリックリンクをパスの通ったディレクトリに張る。

***************
食品管理機能
***************

「日本食品標準成分表2015年版（七訂）」の管理
=============================================

Excel ファイルの入手
--------------------------------------------

日本食品標準成分表2015年版（七訂）の Excel ファイルは以下から入手可能。

`第2章　日本食品標準成分表　Exceｌ（日本語版）：文部科学省 <http://www.mext.go.jp/a_menu/syokuhinseibun/1365420.htm>`_

上記からダウンロードできる「一括ダウンロード（Excel：日本語）  （Excel:917KB）」には全ての食品群の食品が記載されているので、これを利用するのが楽である。

Excel ファイルを Pickle ファイルに変換
--------------------------------------------

日本食品標準成分表2015年版（七訂）の Excel ファイルを Pickle ファイルに変換。

以下の例では、「1　穀類」の Excel ファイル（1365344_1-0201r3.xlsx）を Pickle ファイルに変換している。

.. code-block:: shell

   $ d-manager convert_to_pickle stofc2015r7 --input 1365344_1-0201r3.xlsx > output.pickle

日本食品標準成分表2015年版（七訂）の Excel ファイルを既にある Pickle ファイルに変換する。

以下の例では、「10　魚介類」の Excel ファイル（1365344_1-0210r4.xlsx）を Pickle ファイルに追加している。

.. code-block:: shell

   $ d-manager convert_to_pickle stofc2015r7 --input 1365344_1-0210r4.xlsx --append output.pickle

変換済みの日本食品標準成分表2015年版（七訂）の Pickle ファイルを YAML ファイルとして表示する。

Pickle ファイルを YAML ファイルに変換
--------------------------------------------

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

Excel ファイルを Pickle ファイルに一括変換
--------------------------------------------

ダウンロードページにある「一括ダウンロード（Excel：日本語）  （Excel:917KB）」には全ての食品群の食品が記載されているので、これから Pickle ファイルを作成すれば、以下の方法は不要である。

`bin/convert_stofc2015r7_to_one_pickle.sh` というスクリプトを利用することで、食品群毎に分かれた日本食品標準成分表2015年版（七訂）の Excel ファイルをまとめて `stofc2015r7_all.pickle` という Pickle ファイルに変換可能である。

このスクリプトと同階層に現在（2017年9月）公開されている日本食品標準成分表2015年版（七訂）の Excel ファイル全て（「1　穀類」から「18　調理加工食品類」）を配置してから、このスクリプトを実行する。


   1365344_1-0202r.xlsx   1365344_1-0205r2.xlsx  1365344_1-0208r.xlsx  1365344_1-0211r8.xlsx  1365344_1-0214r9.xlsx
   1365344_1-0217r10.xlsx  d-manager 1365344_1-0203r8.xlsx  1365344_1-0206r8.xlsx  1365344_1-0209.xlsx
   1365344_1-0212r9.xlsx  1365344_1-0215r2.xlsx  1365344_1-0218.xlsx
   $ ./convert_stofc2015r7_to_one_pickle.sh
   append: ./d-manager/bin/1365344_1-0202r.xlsx  to  ./d-manager/bin/stofc2015r7_all.pickle
   ...
   append: ./d-manager/bin/1365344_1-0218.xlsx  to  ./d-manager/bin/stofc2015r7_all.pickle
   $ ls -1 | grep all.pickle
   stofc2015r7_all.pickle


市販食品の管理
===================

概要
--------------------------------------------

市販の食品の栄養成分や商品情報を登録、削除、表示などが出来る。

特に、以下に示す「食品表示法」で表示義務となっている事項から、必要だと思われる事項をこのツールで登録可能な事項ピックアップしている。

「食品表示法」（平成25年法律第70号）及び「食品表示基準」（平成27年内閣府令第10号）では食品の表示に関して種々の基準や義務を定めている。
特に、「栄養成分表示」が義務化され、以下の 5 項目の表示が義務となっている。

* エネルギー（kcal or J）
* タンパク質（g）
* 脂質（g）
* 炭水化物（g）
* 食塩相当量（g）

さらに、名称や内容量、販売者を示す「一括表示」にも各種の基準や指示が定められている。

参考

* `食品表示法等(法令及び一元化情報)｜消費者庁 <http://www.caa.go.jp/foods/index18.html>`_
* `食品表示法 <http://law.e-gov.go.jp/htmldata/H25/H25HO070.html>`_
* `食品表示基準 <http://law.e-gov.go.jp/htmldata/H27/H27F10001000010.html>`_

登録
--------------------------------------------

指定した Pickle ファイルに対話的に食品を追加登録する。
もし、指定したファイルが存在しなければ新規作成する。

以下のように、サブコマンド `add_interactively product_food` を使うことで質問に答えながら指定の Pickle ファイルに食品を登録できる。

.. code-block:: shell

   $ d-manager add_interactively product_food -i product_food.pickle

      1: 穀類, 2: いも及びでん粉類, 3: 砂糖及び甘味類, 4: 豆類,
      5: 種実類, 6: 野菜類, 7: 果実類, 8: きのこ類,
      9: 藻類, 10: 魚介類, 11: 肉類, 12: 卵類,
      13: 乳類, 14: 油脂類, 15: 菓子類, 16: し好飲料類,
      17: 調味料及び香辛料類, 18: 調理加工食品類

     ?> 13
     13: 乳類 が選択されました。

     食品の「商品名」を入力してください。
     注意: 一括表示内の「名称」のことではない。
     ?> 明治ブルガリアヨーグルトLB81プレーン
     明治ブルガリアヨーグルトLB81プレーン が入力されました。

     食品の「名称」を入力してください。
     注意: 包装内の一括表示内の「名称」欄に記載されているもの。
     ?> 醗酵乳
     醗酵乳 が入力されました。

     ... 中略 ...

     脂質を入力してください。単位=gram
     ?> 3.0
     3.0 が入力されました。

     炭水化物を入力してください。単位=gram
     ?> 5.3
     5.3 が入力されました。

     食塩相当量を入力してください。単位=gram
     ?> 0.13
     0.13 が入力されました。

     以下を登録しますが、よろしいですか？
     classification: {group_name: 乳類, group_number: 13, id_in_group: 1}
     food:
       amount: 100 g
       name: 醗酵乳
       nutrient: {carbohydrate: 5.3 g, energy: 62 kcal, lipid: 3.0 g, protein: 3.4 g, salt_equivalent: 0.13
           g}
     id: 130001
     product: {maker: 株式会社 明治, name: 明治ブルガリアヨーグルトLB81プレーン}

     [Y/n]> Y
     1300001 が登録されました。


参照、表示
--------------------------------------------

指定した Pickle ファイルに登録されている食品の一覧を YAML 形式で表示ができる。

以下のように、サブコマンド `view_pickle_as_yaml product_food` を使うことで質問に答えながら指定の Pickle ファイルに食品を登録できる。

.. code-block:: shell

   $ d-manager add_interactively product_food -i product_food.pickle
     - classification: {group_name: 乳類, group_number: 13, id_in_group: 1}
       food:
         amount: 100 g
         name: 醗酵乳
         nutrient: {carbohydrate: 5.3 g, energy: 62 kcal, lipid: 3.0 g, protein: 3.4 g,
           salt_equivalent: 0.13 g}
       id: 130001
       product: {maker: 株式会社 明治, name: 明治ブルガリアヨーグルトLB81プレーン}

削除
--------

指定した Pickle ファイルに登録されている食品から指定した ID の食品を削除できる。

以下のように、サブコマンド `delete product_food` を使う。

.. code-block:: shell

   $nager delete product_food -t 130001 -i /home/bunbun/dev/d-manager/tests/product_food.pickle
    以下を削除しますが、よろしいですか？
    classification: {group_name: 乳類, group_number: 13, id_in_group: 1}
    food:
      amount: 100 g
      name: 醗酵乳
      nutrient: {carbohydrate: 5.3 g, energy: 62 kcal, lipid: 3.0 g, protein: 3.4 g, salt_equivalent: 0.13
          g}
    id: 130001
    product: {maker: 株式会社 明治, name: 明治ブルガリアヨーグルトLB81プレーン}

    [Y/n]> Yes
    id 130001 を削除しました。
