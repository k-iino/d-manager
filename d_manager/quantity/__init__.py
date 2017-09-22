from pint import UnitRegistry

# 実際の物理量の操作は別のパッケージに委任している。
# 異なる UnitRegistry 間だと量同士の演算が出来ないので
# 各種演算がされる量を持つクラスは一つの UnitRegistry を利用する必要がある。
_ureg = UnitRegistry()
