'''
番数计算器
'''
from card import card
from equation import suanshi,equation,gang
from fan import fan, gangfan
from cards import cards


# 以下是和牌无关的番数
MENQING = fan("门清", 1)
DUANYAO = fan("断幺", 2)
QUANDAIYAO = fan("全带幺", 2)
DUANER = fan("断二", 3)
HUNYISE = fan("混一色", 5)
ERTONGSHI = fan("二同式", 5)
JIAYISE = fan("二同式", 10)
SIMENQI = fan("二同式", 10)
QUANHESHU = fan("全合数",15)
CHENGYISE = fan("乘一色",15)


# 以下是和有无关的番数

# 以下是和胡牌方式有关的番数

def calculate(string):
    pass
