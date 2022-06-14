import argparse
from typing import List, Dict
import pandas as pd
import numpy as np
from PIL import Image
from pandas.core.frame import DataFrame
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import getFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm


# IPAexフォント
IPA_EX_M_TTF = "./fonts/IPAexfont/ipaexm.ttf"
IPA_EX_G_TTF = "./fonts/IPAexfont/ipaexg.ttf"


class NengaPdf:
    """年賀状のPDFクラス"""    
    def set_up(self, fname='address.pdf') -> canvas.Canvas:
        """
        フォント設定とpdfのサイズを設定
        """
        pdfmetrics.registerFont(TTFont('IPAexm', IPA_EX_M_TTF))
        pdfmetrics.registerFont(TTFont('IPAexg', IPA_EX_G_TTF))
        pdf = canvas.Canvas(fname)
        pdf.setPageSize((10 * cm, 14.8 * cm))
        return pdf
    
    def draw_image(self, pdf: canvas.Canvas):
        """
        pdfの背景画像設置
        """
        image = Image.open('./layout_nenga.png')
        pdf.drawInlineImage(image, 2, 0, width=10 * cm, height=14.8 * cm)
        
    def draw_zipcode(self, pdf: canvas.Canvas, zipcode):
        """
        郵便番号をpdfに配置する
        """
        # 文字サイズ
        ZIP_CODE_FONT_SIZE = 15
        # 文字間隔（パディング）
        ZIP_CODE_FONT_PADDING = 24
        # 文字間隔（マージン）
        ZIP_CODE_FONT_MARGIN = 0.17 * cm
    # ハイフン付き郵便番号をハイフンなしにする（pdf上ハイフン表示が不要なため）
        if "-" in zipcode:
            zipcode = zipcode.replace('-', '')

        pdf.setFont('IPAexg', ZIP_CODE_FONT_SIZE)
        width_char = getFont('IPAexg').stringWidth(
            zipcode[0], ZIP_CODE_FONT_PADDING) + ZIP_CODE_FONT_MARGIN
        for i, c in enumerate(zipcode):
            x = 4.6 * cm + width_char * i
            y = 13 * cm
            pdf.drawString(x, y, c)
            
n001 = NengaPdf()


def draw_zipcode_owner(pdf: canvas.Canvas, zipcode):
    """
    送り元郵便番号
    """
    # 文字サイズ
    _ZIP_CODE_FONT_SIZE = 13
    # 文字間隔（パディング）
    _ZIP_CODE_FONT_PADDING = 10
    # 文字間隔（マージン）
    _ZIP_CODE_FONT_MARGIN = 0.17 * cm

    if "-" in zipcode:
        zipcode = zipcode.replace('-', '')

    pdf.setFont('IPAexg', _ZIP_CODE_FONT_SIZE)
    _width_char = getFont('IPAexg').stringWidth(
        zipcode[0], _ZIP_CODE_FONT_PADDING) + _ZIP_CODE_FONT_MARGIN

    for i, c in enumerate(zipcode):
        # 微調整
        if i > 2:
            x = 0.81 * cm + _width_char * i
        else:
            x = 0.66 * cm + _width_char * i
        y = 2 * cm
        pdf.drawString(x, y, c)


def draw_send_name(pdf: canvas.Canvas, df_send_name: DataFrame):
    """
    宛先の氏名（連名にも対応）
    """
    # 文字サイズ
    SEND_ADDRES_1_FONT_SIZE = 20

    pdf.setFont('IPAexm', SEND_ADDRES_1_FONT_SIZE)

    base_y = 10.5 * cm

    if len(df_send_name) == 1:
        base_x = 5.1 * cm
    elif len(df_send_name) == 2:
        base_x = 6.1 * cm
    elif len(df_send_name) == 3:
        base_x = 6.1 * cm
    elif len(df_send_name) == 4:
        base_x = 6.6 * cm
    elif len(df_send_name) == 5:
        base_x = 7.1 * cm

    MARGIN = 1 * cm

    # 連名の横間隔
    side_width = 0.8 * cm

    names = edit_names(df_send_name)

    for i_owner_names, name in enumerate(names):
        x = base_x - side_width * i_owner_names
        y = base_y
        for i, c in enumerate(name):
            y = base_y - MARGIN * i
            pdf.drawString(x, y, c)


def edit_names(df_name: DataFrame):

    df_name = df_name.fillna('')

    max_sei = df_name[0].map(lambda x: len(x)).max()
    max_mei = df_name[1].map(lambda x: len(x)).max()

    owner_names = []
    for sei_mei in df_name.values:
        # 姓・名ループ
        owner_name = ""
        for i_sei_mei, sm in enumerate(sei_mei):
            # 姓が空の場合は全角スペースで埋める
            if i_sei_mei == 0 and len(sm) == 0:
                owner_name = "　" * max_sei
            else:
                # sprint(f'{sm} {max_mei}')
                if i_sei_mei == 1 and len(sm) < max_mei:
                    owner_name = owner_name + sm + "　" * (max_mei - len(sm))
                else:
                    owner_name = owner_name + sm
        owner_names.append(owner_name)

    return owner_names


def draw_name_owner(pdf: canvas.Canvas, names: DataFrame):
    """
    送り元氏名（連名にも対応）
    """
    # 文字サイズ
    SEND_ADDRES_1_FONT_SIZE = 9.5

    pdf.setFont('IPAexm', SEND_ADDRES_1_FONT_SIZE)

    base_y = 5.8 * cm

    if len(names) == 1:
        base_x = 0.5 * cm
    elif len(names) == 2:
        base_x = 1.1 * cm
    elif len(names) == 3:
        base_x = 1.5 * cm

    MARGIN = 0.6 * cm

    # 連名の横間隔
    side_width = 0.4 * cm

    # 連名ループ
    owner_names = edit_names(names)

    for i_owner_names, name in enumerate(owner_names):
        x = base_x - side_width * i_owner_names
        y = base_y
        for i, c in enumerate(name):
            y = base_y - MARGIN * i
            pdf.drawString(x, y, c)


def edit_address(address: List):
    """
    宛先住所に適度に改行をいれて整形
    （TODO: リファクタリングしたい）
    """
    list_edited = []
    address_length = 0
    address_char = ""

    for ad in address:
        ad = str(ad)
        address_length = address_length + len(ad)
        if (address_length > 16):
            list_edited.append(address_char)
            # リセット
            address_length = len(ad)
            address_char = ad
            continue

        address_char = address_char + ad

    list_edited.append(address_char)
    return list_edited


def draw_send_address(pdf: canvas.Canvas, address: List):
    """
    宛先住所
    """
    # 文字サイズ
    SEND_ADDRES_1_FONT_SIZE = 14

    pdf.setFont('IPAexm', SEND_ADDRES_1_FONT_SIZE)

    for addr_i, addr_word in enumerate(address):
        addr_x = 8.7 * cm - 0.6 * cm * addr_i

        for i, c in enumerate(addr_word):
            y = 12 * cm - (0.5 * cm * i)

            # 住所の番地前後のハイフンの文字サイズ変更
            if c in '-ー－':
                pdf.setFont('IPAexm', 8)
                pdf.drawString(addr_x+6, y+2, chinese_numeral(c))
            else:
                pdf.setFont('IPAexm', SEND_ADDRES_1_FONT_SIZE)
                pdf.drawString(addr_x, y, chinese_numeral(c))


def draw_send_address_owner(pdf: canvas.Canvas, address: List):
    """
    送り元住所
    """
    # 文字サイズ
    SEND_ADDRES_1_FONT_SIZE = 10.5

    pdf.setFont('IPAexm', SEND_ADDRES_1_FONT_SIZE)

    for addr_i, addr_word in enumerate(address):
        addr_x = 2.8 * cm - 0.5 * cm * addr_i

        for i, c in enumerate(addr_word):
            y = 8.5 * cm - (11 * i)

            # 住所の番地前後のハイフンの文字サイズ変更
            if c in '-ー－':
                pdf.setFont('IPAexm', 6)
                pdf.drawString(addr_x+5, y+2, chinese_numeral(c))
            else:
                pdf.setFont('IPAexm', SEND_ADDRES_1_FONT_SIZE)
                pdf.drawString(addr_x, y, chinese_numeral(c))


def chinese_numeral(s):
    convert_table = {ord(u'0'): u'〇', ord(u'1'): u'一', ord(u'2'): u'二',
                     ord(u'3'): u'三', ord(u'4'): u'四', ord(u'5'): u'五',
                     ord(u'6'): u'六', ord(u'7'): u'七', ord(u'8'): u'八',
                     ord(u'9'): u'九', ord(u'-'): u'|', ord(u'－'): u'|', 
                     ord(u'ー'): u'|'}
    return s.translate(convert_table)


def drow_owner_info(pdf, owner_info: Dict):
    """
    送り元情報
    """
    zipcode = owner_info["zipcode"]
    draw_zipcode_owner(pdf, zipcode)
    address = owner_info["address"]
    draw_send_address_owner(pdf, address)
    names = owner_info["names"]
    draw_name_owner(pdf, names)


if __name__ == '__main__':

    # コマンドライン引数
    parser = argparse.ArgumentParser()
    parser.add_argument("--layout", help="optional", action="store_true")
    args = parser.parse_args()

    nenga_pdf = NengaPdf()
    pdf = nenga_pdf.set_up()

    df_send = pd.read_csv('address_list.csv').fillna('')
    df_owner = pd.read_csv('owner_info.csv').fillna('')

    # 送り元郵便番号
    owner_zipcode = df_owner.iloc[0]['郵便番号(自宅欄)']
    # 送り元住所
    owner_address = [
        df_owner.iloc[0]['自宅住所(都道府県)'],
        df_owner.iloc[0]['自宅住所(市区町村)'],
        df_owner.iloc[0]['自宅住所(番地等)'],
        df_owner.iloc[0]['自宅住所(建物名)'],
    ]
    # 送り元氏名
    owner_names = [
        [str(df_owner.iloc[0]["氏名(姓)"]), str(df_owner.iloc[0]["氏名(名)"])],
        [str(df_owner.iloc[0]["連名1(姓:自宅欄)"]),
         str(df_owner.iloc[0]["連名1(名:自宅欄)"])],
        [str(df_owner.iloc[0]["連名2(姓:自宅欄)"]),
         str(df_owner.iloc[0]["連名2(名:自宅欄)"])],
    ]
    df_names_owner = pd.DataFrame(
        data=owner_names
    )

    for i, row in df_send.iterrows():
        # 年賀状レイアウト出力
        if args.layout:
            nenga_pdf.draw_image(pdf)

        # 送り先住所
        send_address = edit_address(
            [
                str(row['自宅住所(都道府県)']),
                str(row['自宅住所(市区町村)']),
                str(row['自宅住所(番地等)']),
                str(row['自宅住所(建物名)']),
            ]
        )

        # 送り先氏名
        send_name = [
            [str(row["氏名(姓)"]), str(row["氏名(名)"]), str(row["敬称"])],
            [str(row["連名1(姓:自宅欄)"]),
             str(row["連名1(名:自宅欄)"]),
                str(row["連名1(敬称:自宅欄)"])],
            [str(row["連名2(姓:自宅欄)"]),
             str(row["連名2(名:自宅欄)"]),
                str(row["連名2(敬称:自宅欄)"])],
            [str(row["連名3(姓:自宅欄)"]),
             str(row["連名3(名:自宅欄)"]),
                str(row["連名3(敬称:自宅欄)"])],
            [str(row["連名4(姓:会社欄)"]),
             str(row["連名4(名:会社欄)"]),
                str(row["連名4(敬称:会社欄)"])],
            [str(row["連名5(姓:会社欄)"]),
             str(row["連名5(名:会社欄)"]),
                str(row["連名5(敬称:会社欄)"])],
        ]
        df_send_name: DataFrame = pd.DataFrame(data=send_name)
        df_send_name = df_send_name.replace("", np.nan)
        df_send_name = df_send_name.dropna(how='all', axis=0)

        nenga_pdf.draw_zipcode(pdf, str(row['郵便番号(自宅欄)']))
        draw_send_address(pdf, send_address)
        draw_send_name(pdf, df_send_name)

        # 送り元
        owner_info = {
            "zipcode": owner_zipcode,
            "address": edit_address(owner_address),
            "names": df_names_owner
        }

        drow_owner_info(pdf, owner_info)

        # 改ページ
        pdf.showPage()

    # PDF保存
    pdf.save()
