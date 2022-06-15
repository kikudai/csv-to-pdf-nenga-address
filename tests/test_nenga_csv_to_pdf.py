import nenga_csv_to_pdf as nenga
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from nenga_csv_to_pdf import *

def test_draw_zipcode():
    assert "a"=="a"
  
def test_draw_zipcode_owner():
    n001=nenga.NengaPdf()
    result=n001.draw_zipcode("262-0024")
    assert result=="2620024"

def test_draw_send_name():
    

    