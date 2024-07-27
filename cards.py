'''
cards这个是代表的整套卡的格式，待定
目前定的格式是：
你的牌 & 单张杠的牌 & 开口的牌
如果没有开口的牌，只有一个&即可
有就必须两个&都要
如果单张杠和开口的都没有，那就不用
牌的格式：
前两位代表牌正面信息，后面代表其他信息
前两位：数字是数字，符号是符号，万用：后面加w。
不定：小（0-9），中（10-19），大（20+），符号万用分别是ws, wm, wl, wo
万字是：几万就几m
例如：
宝牌13： 13d
一般13： 13
符号万用牌代替乘号：*w
大万用代替22：22w
大万用（不确定）：wl
两万（不确定）：2m
听的牌用括号表示。
注意：请一定带上前缀，否则会区分不开：例如24可能是万用24，可能是4万的24，19可能带宝牌，
不带宝牌也可能是万用。
注意：可能只有前缀，但是没有实际值。
注意：必须标明胡法，有区分一定要区分，分数牌型不用
例子1：
(1) + 2 3 | 2 + 3 5 & 11d & 6 + 7 13 | 9 + 10 19
表示的是：
我手牌2 + 3 2 + 3 5，此时有宝牌11杠出，并且吃了6+7=13以及9+10=19
此时我胡牌1凑成1+2=3
例子2：
(32) 32 10w 10 11 11d 14 14 16 16 18 18 20 20 25w 25 & 13d ws
表示的是：
我手牌两个两万当做32，一个10-19万用当做10，一个10，一个11，一个11宝牌，两个14,16,18,
20，一个五万当做25，一个20+万用牌当做25。杠出来了一个宝牌13，和0-9万用，此时我摸到一
张两万，胡八小对。
注意！有特殊牌型！
'''
from card import card
from equation import suanshi, equation, gang

# 特殊牌型
BAXIAODUI = "八小对"
SHISANYAO = "十三幺"
SHILIUXI = "十六稀"
HUNLONG = "混龙"
QINGLONG = "清龙"

class cards:
    def __init__(self, cards_string:str):
        self.equation_set = [] # 整理出所有的算式，如果有
        self.is_special = False # 看是否是特殊牌型
        self.special = None # 如果是特殊牌型，这个是什么牌型
        self.value_set = [] # 牌的值的集合
        self.card_set = [] # 牌的集合
        self.value_set_dora_incl = [] # 牌的值的集合，包括宝牌
        self.card_set_dora_incl = [] # 牌的集合，包括宝牌
        self._parse(cards_string)
        if self.is_special:
            self.special = self._judge_special()
        pass
    
    def _parse(self, card_string):
        # 将卡牌变成卡的集合，先粗略区分三者
        yours, dora, kaikou = [], [], []
        lst = card_string.split("&")
        yours = (lst[0].strip()).split("|")
        if len(lst) >= 2:
            dora = (lst[1].strip()).split(" ")
        if len(lst) >= 3:
            kailou = (lst[2].strip()).split("|")
        print(yours, dora, kaikou)
        
        # 将每一个东西变成算式或者杠
        yours_short = []
        total_yours = 0
        for suanshi in yours:
            suanshi.strip()
            lst = suanshi.strip().split(" ")
            suanshi_card_list = [card(cd) for cd in suanshi]
            total_yours += len(suanshi_card_list)
            eqn, is_special = self._suanshify(suanshi_card_list)
            if is_special:
                self.is_special = True
            yours_short.append(eqn)
        
        # 处理宝牌
        print("快做处理宝牌！")
        
        # 处理宝牌
        print("快做面子上的牌！")
        pass
    
    def _suanshify(self, suanshi_card_list):
        # 将字符串组合变成算式或者杠
        assert len(suanshi_card_list)>=4, "算式长度不对：是不是漏牌了？"
        if len(suanshi_card_list)>4:
            # 特殊牌组(16张)，或者多张杠
            is_same_card = True
            number = suanshi_card_list[0].actual
            for cd in range(suanshi_card_list):
                if cd.actual != number:
                    is_same_card = False
            if is_same_card:
                # 是多张杠
                return gang(number,len(suanshi_card_list)), False
            else:
                # 是特殊胡法，此时手牌应该16张
                assert len(suanshi_card_list) == 16, "看起来是特殊胡法，但是牌数是不是不对？"
                return suanshi_card_list, True
        else:
            # 普通的四张的一句话
            print("快做一般情况！")
        pass
    
    def _judge_special(self):
        # 初步检测什么特殊胡法，等待弄
        print("快做特殊胡法！")
        pass