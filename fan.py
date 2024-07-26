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