from pint import UnitRegistry

# 実際の物理量の操作は別のパッケージに委任している。
# 異なる UnitRegistry 間だと量同士の演算が出来ないので
# 各種演算がされる量を持つクラスは一つの UnitRegistry を利用する必要がある。
_ureg = UnitRegistry()


class _Quantity:
    """
    物理量のクラス

    pint の物理量クラスの簡易的なラッパ。
    """
    def __init__(self, magnitude, unit):
        self.q = _ureg.Quantity(magnitude, unit)

    def to(self, unit):
        """単位を変換する"""
        self.q = self.q.to(unit)
        return self

    def round(self, ndigit):
        """物理量の値を小数点以下第 N 位に丸め込む"""
        m = round(self.q.m, ndigit)
        self.q = _ureg.Quantity(m, self.q.u)
        return self

    def __str__(self):
        return '{:~P}'.format(self.q)

    def __add__(self, other):
        # pint を利用して生成した Quantity や Unit は同一の UnitRegister インスタンスから
        # 生成したもの同士でないと比較や各種演算が出来ない。
        # そのため、Pickle 形式などでシリアライズした Quantity や Unit をデシリアライズして
        # 再利用しようとするとエラーが発生する。
        # そのため、シリアライズをする場合は物理量の演算か、入出力の実装を変更する必要がある。
        self.q += other.q
        return self

    def __mul__(self, other):
        self.q *= other
        return self

    @classmethod
    def from_str(cls, input_str):
        """文字列から単位を作成"""
        _pq = _ureg.parse_expression(input_str)
        return cls(_pq.magnitude, _pq.units)

    @property
    def magnitude(self):
        """Quantity's magnitude. Long form for `m`
        """
        return self.q.magnitude

    @property
    def m(self):
        """Quantity's magnitude. Short form for `m`
        """
        return self.q.magnitude

    @property
    def unit(self):
        """Quantity's units. Long form for `u`
        """
        return self.q.units

    @property
    def u(self):
        """Quantity's units. Short form for `units`
        """
        return self.q.units
