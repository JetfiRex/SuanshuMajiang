'''
cards这个是代表的整套卡的格式，待定
目前定的格式是：
你的牌 & 宝牌 & 面上的牌
牌的格式：
前两位代表牌正面信息，后面代表其他信息
前两位：数字是数字，符号是符号，万用：0-9万用：ws（wildcard small），10-19万用：wm
（wildcard medium），20+万用：wl（wildcard large），符号万用：wo（wildcard operator）
万字是：几万就几m
例如：
宝牌13： 13d
一般13： 13
符号万用牌代替乘号：op*
两万代替42：2m42
注意：请一定带上前缀，否则会区分不开：例如24可能是万用24，可能是4万的24，19可能带宝牌，
不带宝牌也可能是万用。
注意：可能只有前缀，但是没有实际值。
'''
from card import card

class cards:
    def __init__(self, cards_string):
        pass