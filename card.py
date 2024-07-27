"""
card类，表示一张卡
注意要区分面值以及实际值
"""

class card:
    
    possibilities = {
        "wo" :["+", "*", "^"],
        "ws" : list(range(10)),
        "wm" : list(range(10,20)),
        "wl" : list(range(20,50)),
        }|{
        str(i)+"m" : [i+20, i+30, i+40] for i in range(10)}
    
    def __init__(self, string):
        
        self.face = None # 一律为str格式
        self.actual = None # str格式（符号）或者int格式（数字）或者str/int的list（未定）
        self.is_dora = None # 一律为bool格式
        self._assign(string)
    
    def _assign(self,card_string):
        # 支持的格式：
        # 纯数字或者确定的万字/符号：数字/符号本身
        # 用万用代替的数字符号：数字/符号本身+w
        # 带宝牌的数字：数字+d
        # 不确定万用：小万用，中万用，大万用，符号万用：ws, wm, wl, wo
        # 未确定万字：万字本身加m
        # 其他格式亟待发掘和兼容
        if "d" in card_string:
            # 宝牌
            self.face = card_string
            self.actual = eval(card_string[:-1])
            self.is_dora = True
            return
        # 因为单张杠万用不会指定数字
        self.is_dora = False
        if "m" not in card_string and "w" not in card_string:
            # 纯数字或者符号
            if card_string[0] in ["*", "+", "^"]:
                # 符号牌
                self.face = self.actual = card_string[0]
            else:
                # 纯数字牌
                self.actual = eval(card_string)
                if self.actual > 20 and self.actual != 30:
                    # 是万字
                    self.face = card_string[1]+"m"
                else:
                    self.face = card_string
        elif "m" in card_string or card_string[0] == "w":
            # 是未定万字或者未定万用
            self.face = card_string
            self.actual = self.possibilities[card_string]
        else:
            if card_string[0] in ["*", "+", "^"]:
                # 定下符号的万用牌
                self.face = "wo"
                self.actual = card_string[0]
            else:
                # 定下数字的万用牌
                self.actual = eval(card_string[:-1])
                if self.actual >= 20:
                    # 是大万用
                    self.face = "wl"
                elif self.actual < 20 and self.actual >= 10:
                    # 是中万用
                    self.face = "wm"
                else:
                    # 是小万用
                    self.face = "ws"
    
    def __str__(self):
        return f"面值{self.face}，表示{self.actual}，"+(1-self.is_dora)*"不"+"是宝牌"