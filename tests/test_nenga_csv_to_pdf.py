import nenga_csv_to_pdf as nenga
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm


# IPAexフォント
IPA_EX_M_TTF = "./fonts/IPAexfont/ipaexm.ttf"
IPA_EX_G_TTF = "./fonts/IPAexfont/ipaexg.ttf"

def test_set_up(fname='address.pdf'):
    """フォント設定とpdfのサイズを設定"""
    pdfmetrics.registerFont(TTFont('IPAexm', IPA_EX_M_TTF))
    pdfmetrics.registerFont(TTFont('IPAexg', IPA_EX_G_TTF))
    pdf = canvas.Canvas(fname)
    pdf.setPageSize((10 * cm, 14.8 * cm))

    assert pdf != None


def test_draw_zipcode():
    resolt=nenga.draw_zipcode(None, "262-0024")
    assert resolt=="2620024"
