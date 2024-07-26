'''
fan 代表番数这一类。番数包括名字，类别，以及信息
'''

class fan:
    def __init__(self, name, amount, info = None):
        self.name = name
        self.amount = amount
        self.info = info
    
    def __str__(self):
        if self.info is None:
            return f"{self.name}，{self.amount}番。"

class gang(fan):
    def __init__(self, card, n, show):
        self.name = self.get_name(card,n,show)
        self.amount = self.get_amount(card,n,show)
    
    def get_name(card,n,show):
        # 计算他应该叫的名字
        # 如果是单张杠，就是“单张杠X”
        # 如果是多张杠，区分是“明杠”还是“暗杠”，并且说明点数和张数
        pass
    
    def get_amount(card,n,show):
        # 计算他应该的番数
        # 如果是单张杠，一番
        # 如果是多张杠，区分是明暗杠，暗杠多一番。
        pass