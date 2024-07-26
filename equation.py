'''
suanshi 代表算式这一类。算式包括运算信息，番数和结果等信息。
suanshi包括两类，一类是真的算式（equation类），一类是杠（gang）
gang分为单张杠(single_gang)和多张杠(gang)
'''

# Python program showing
# abstract base class work
from abc import ABC, abstractmethod

class suanshi:
    def __init__(self):
        self.type = None
        self.fan = 0
        self.raw = None
    
    @abstractmethod
    def __str__(self):
        pass
    

class equation(suanshi):
    
    def __init__(self,a,op,b,c):
        self.type = op
        self.raw = [a,op,b,c]
    
    def dora(self):
        # 检测是否含有宝牌
        pass
    
    def __str__(self):
        pass

class gang(suanshi):
    def __init__(self,a,n=4):
        self.raw = [a,n]
        if n == 1:
            self.type = "single_gang"
        else:
            self.type = "gang"
    
    def __str__(self):
        pass
    
    def fan(self):
        #计算这个杠的番数
        pass