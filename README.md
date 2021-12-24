# 年賀状宛名 csv の pdf 化
csvファイル（はがきデザインキット）から、年賀状宛名をpdfにして印刷できるようにする。

## 概要
はがきデザインキットが機能停止してしまい、過去のcsvなど利用できなくなっていた。
これはもう python で印刷するしかない。

## 機能
はがきデザインキットから書き出した宛名csvをpdfにする

## サンプルコマンド
```
# 年賀状レイアウト付きでpdf出力（pdfでレイアウト確認をしたいとき）
python nenga_csv_to_pdf.py --layout

# 年賀状レイアウトなしでpdf出力（はがき宛名面印刷をするとき）
python nenga_csv_to_pdf.py
```
## サンプル
![sample_nenga](https://github.com/kikudai/csv-to-pdf-nenga-address/blob/main/sample_nenga.png)

## 事前準備
### python のインストール
* [Python環境構築ガイド - python.jp](https://www.python.jp/install/install.html) などを参考に python をインストール

### コマンド実行環境構築
```
git clone https://github.com/kikudai/csv-to-pdf-nenga-address.git
cd csv-to-pdf-nenga-address.git

# ライブラリインストール
pip install -r require
```

### コマンド実行
owner_info.csv、address_list を nenga_csv_to_pdf.py と同じディレクトリ配下においてコマンド実行する。
address_list.csv は、はがきデザインキットから書き出したcsvファイルのことです。
owner_info.csv はサンプルcsvを参考に自身の住所・氏名の csv を作成してください。
```
# まずはサンプルcsvファイルをコピー
cp ./sample_csv/*.csv ./

# コマンド実行後、address.pdf が作成される
python nenga_csv_to_pdf.py --layout
```

## 注意事項
* csvファイル（年賀状住所、送り元情報）の文字コードは utf8 にする
* pdf を Adobe acrobat reader DC などで開きっぱなしのとき、コマンド実行するとエラー（PermissionError: [Errno 13] Permission denied: 'address.pdf'）になるので閉じて実行する

## 感想
* 作成期間約2日、本当は半日くらいで作りたかった
* ここのコードをもとに作成しました。ありがたや。これがなければ、もう1日くらいかかっていそう  
https://github.com/satemochi/saaaaah/blob/master/misc/new_year_card/write_address.py 
* 恥ずかしコード、リファクタリングすれば半分くらいのコードになりそう
