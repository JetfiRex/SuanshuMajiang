'''
番数计算器
'''
from card import card
from equation import suanshi,equation,gang
from fan import fan, card_dependent_fan
from cards import cards

# 以下是能胡的番数

ERTONGSHI = fan("二同式", 5)
HUNYISE = fan("混一色", 5)
SIMENQI = fan("四门齐", 10)
JIAYISE = fan("加一色", 10)
QUANHESHU = fan("全合数",15)
CHENGYISE = fan("乘一色",15)

# 以下是不能胡，和牌无关的番数

MENQING = fan("门清", 1)
DUANYAO = fan("断幺", 2)
QUANDAIYAO = fan("全带幺", 2)
DUANER = fan("断二", 3)


# 以下是不能胡，和有无关的番数

# 以下是和胡牌方式有关的番数

def calculate(card_set):
    if type(card_set) == str:
        card_set = cards(card_set)
    pass
