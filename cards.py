'''
cards这个是代表的整套卡的格式，待定
目前定的格式是：
你的牌 & 单张杠的牌 & 开口的牌
如果没有开口的牌，只有一个&即可
有就必须两个&都要
如果单张杠和开口的都没有，那就不用
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
听的牌用括号表示。
注意：请一定带上前缀，否则会区分不开：例如24可能是万用24，可能是4万的24，19可能带宝牌，
不带宝牌也可能是万用。
注意：可能只有前缀，但是没有实际值。
注意：必须标明胡法，有区分一定要区分，分数牌型不用
例子1：
(1) + 2 3 | 2 + 3 5 & 11d & 6  + 7 13 | 9 + 10 19
表示的是：
我手牌2 + 3 2 + 3 5，此时有宝牌11杠出，并且吃了6+7=13以及9+10=19
此时我胡牌1凑成1+2=3
例子2：
(2m32) 2m32 wm10 10 11 11d 14 14 16 16 18 18 20 20 wl25 5m25 & 13d ws
表示的是：
我手牌一个两万当做32，一个10-19万用当做10，一个10，一个11，一个11宝牌，两个14,16,18,
20，一个五万当做25，一个20+万用牌当做25。杠出来了一个宝牌13，和0-9万用，此时我摸到一
张两万，胡八小对。
注意！有特殊牌型！
'''
from card import card

# 特殊牌型
BAXIAODUI = "八小对"

class cards:
    def __init__(self, cards_string:str):
        self.equation_set = [] # 整理出所有的算式，如果有
        self.is_special = False # 看是否是特殊牌型
        self.special = None
        self.value_set = [] # 牌的值的集合
        self.card_set = [] # 牌的集合
        self.value_set_dora_incl = [] # 牌的值的集合，包括宝牌
        self.card_set_dora_incl = [] # 牌的集合，包括宝牌
        self._parse(cards_string)
        pass
    
    def _parse(self, card_string):
        # 将卡牌变成卡的集合
        yours, dora, kaikou = [], [], []
        card_string
        pass