import pytest


class TestNengaPdf():
    """NengaPdfクラスのテスト"""

    @pytest.mark.parametrize(
        'test_zipcode',
        ['191-0053','1-910053','1910053-']
    )
    def test_draw_zipcode_1(self, test_zipcode):
        """郵便番号からハイフンを取り除く"""
        # （前提）特になし
        # （いつ）文字列中に半角ハイフンが含まれていたら半角ハイフンのみを除外
        # （結果）半角ハイフン除外
        test_zipcode == '1910053'
