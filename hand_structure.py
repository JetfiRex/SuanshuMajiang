"""
算术麻将手牌数据结构
定义牌、鸣牌面子、手牌等数据结构
"""

from typing import List, Optional, Union
from parser import SYMBOLS, JOKERS, PLUS, MULTIPLY, POWER


class Tile:
    """
    单张牌的数据结构
    
    属性：
        value: 牌值（int数字或str符号）
        is_dora: 是否是宝牌/dora（11d, 13d, 17d, 19d）
        is_joker_used: 是否是万用牌代替的
        joker_type: 原始万用牌类型（如果是万用牌代替的）
    """
    
    # 宝牌列表（dora tiles）
    DORA_TILES = {11, 13, 17, 19}
    
    def __init__(
        self, 
        value: Union[int, str],
        is_dora: bool = False,
        is_joker_used: bool = False,
        joker_type: Optional[str] = None
    ):
        self.value = value
        self.is_dora = is_dora  # 只有显式传入True才是宝牌
        self.is_joker_used = is_joker_used
        self.joker_type = joker_type  # 'tiao', 'tong', 'wan', 'symbol'
        
        # 注意：不再自动设置宝牌标记
        # 只有用户显式标记为 11d, 13d, 17d, 19d 的才是宝牌
    
    def __repr__(self):
        """字符串表示"""
        result = str(self.value)
        if self.is_dora:
            result += 'd'
        if self.is_joker_used:
            result += 'w'
        return result
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        """相等性比较"""
        if not isinstance(other, Tile):
            return False
        return (self.value == other.value and 
                self.is_dora == other.is_dora and
                self.is_joker_used == other.is_joker_used)
    
    def __hash__(self):
        """哈希值（用于set/dict）"""
        return hash((self.value, self.is_dora, self.is_joker_used))
    
    @staticmethod
    def infer_joker_type(value: Union[int, str]) -> Optional[str]:
        """
        从代替值推断原始万用牌类型
        
        参数：
            value: 代替的值
        
        返回：
            'tiao', 'tong', 'wan', 'symbol' 或 None
        """
        if isinstance(value, str) and value in SYMBOLS:
            return 'symbol'
        elif isinstance(value, int):
            if 0 <= value <= 9:
                return 'tiao'
            elif 10 <= value <= 19:
                return 'tong'
            elif 20 <= value <= 49:
                return 'wan'
        return None
    
    def to_simple_value(self):
        """
        转换为简单值（用于与旧代码兼容）
        返回: int 或 str
        """
        return self.value


class MeldedGroup:
    """
    鸣牌面子数据结构
    
    属性：
        tiles: 牌的列表
        group_type: 面子类型
            - 'chi': 吃（4张算式）
            - 'peng': 碰（4张刻子）
            - 'gang_ming': 明杠（5张）
            - 'gang_an': 暗杠（5张）
            - 'single_gang': 单张杠（1张宝牌或万用牌）
    """
    
    VALID_GROUP_TYPES = {'chi', 'peng', 'gang_ming', 'gang_an', 'single_gang'}
    
    def __init__(self, tiles: List[Tile], group_type: str):
        self.tiles = tiles
        self.group_type = group_type
        
        if group_type not in self.VALID_GROUP_TYPES:
            raise ValueError(f"无效的面子类型: {group_type}")
        
        # 验证面子张数
        if group_type == 'single_gang':
            if len(tiles) != 1:
                raise ValueError(f"单张杠必须是1张牌，实际{len(tiles)}张")
        elif group_type in ['gang_ming', 'gang_an']:
            if len(tiles) != 5:
                raise ValueError(f"杠必须是5张牌，实际{len(tiles)}张")
        elif group_type in ['chi', 'peng']:
            if len(tiles) != 4:
                raise ValueError(f"吃/碰必须是4张牌，实际{len(tiles)}张")
    
    def __repr__(self):
        """字符串表示"""
        tiles_str = ' '.join(str(t) for t in self.tiles)
        
        if self.group_type == 'single_gang':
            return f"({tiles_str})"
        elif self.group_type == 'gang_ming':
            return f"({tiles_str} 明)"
        elif self.group_type == 'gang_an':
            return f"({tiles_str} 暗)"
        else:  # chi, peng
            return f"({tiles_str})"
    
    def __str__(self):
        return self.__repr__()
    
    def tile_count(self) -> int:
        """返回面子的牌数（用于计算总牌数）"""
        return len(self.tiles)
    
    def to_simple_tiles(self) -> List[Union[int, str]]:
        """
        转换为简单牌列表（用于与旧代码兼容）
        返回: List[int | str]
        """
        return [tile.to_simple_value() for tile in self.tiles]


class Hand:
    """
    完整手牌数据结构
    
    属性：
        melded_groups: 鸣牌面子列表
        hand_tiles: 手牌列表
        hand_groups: 手牌分组（仅模式1使用，已分好的算式）
        winning_tile: 胡的牌（仅模式1和2使用）
        winning_method: 胡牌方式（仅模式1使用：自摸/点胡/抢杠等）
        win_type: 胡牌类型（"算术麻将"/"传统麻将"/"八小对"，用于防止番数计算时违反不拆移原则）
    """
    
    def __init__(
        self,
        melded_groups: Optional[List[MeldedGroup]] = None,
        hand_tiles: Optional[List[Tile]] = None,
        hand_groups: Optional[List[List[Tile]]] = None,
        winning_tile: Optional[Tile] = None,
        winning_method: Optional[str] = None,
        win_type: Optional[str] = None
    ):
        self.melded_groups = melded_groups or []
        self.hand_tiles = hand_tiles or []
        self.hand_groups = hand_groups or []
        self.winning_tile = winning_tile
        self.winning_method = winning_method
        self.win_type = win_type  # "算术麻将", "传统麻将", "八小对" 或 None
    
    def __repr__(self):
        """字符串表示"""
        parts = []
        
        # 鸣牌
        if self.melded_groups:
            melded_str = ' '.join(str(g) for g in self.melded_groups)
            parts.append(melded_str)
        
        # 手牌（如果有分组则显示分组，否则显示原始手牌）
        if self.hand_groups:
            # 模式1：显示分组
            hand_str = ' / '.join(
                ' '.join(str(t) for t in group) 
                for group in self.hand_groups
            )
            parts.append(hand_str)
        elif self.hand_tiles:
            # 其他模式：显示原始手牌
            hand_str = ' '.join(str(t) for t in self.hand_tiles)
            parts.append(hand_str)
        
        result = ' '.join(parts)
        
        # 胡牌标记
        if self.winning_tile:
            result += f" [{self.winning_tile.value}]"
        
        # 胡牌方式
        if self.winning_method:
            result += f" {{{self.winning_method}}}"
        
        return result
    
    def __str__(self):
        return self.__repr__()
    
    def total_tile_count(self) -> int:
        """
        计算总牌数（不包括杠牌）
        
        公式：(鸣牌面子数 × 4) + 手牌数
        注意：杠牌不计入此公式
        """
        melded_count = 0
        for group in self.melded_groups:
            if group.group_type not in ['gang_ming', 'gang_an', 'single_gang']:
                melded_count += 1  # 每个吃/碰算1组（4张）
        
        return melded_count * 4 + len(self.hand_tiles)
    
    def actual_tile_count(self) -> int:
        """
        计算实际持有的牌数（包括杠牌）
        """
        melded_tiles = sum(g.tile_count() for g in self.melded_groups)
        return melded_tiles + len(self.hand_tiles)
    
    def to_simple_hand(self) -> List[Union[int, str]]:
        """
        转换为简单手牌列表（用于与旧代码兼容）
        只返回手牌部分，不包括鸣牌
        
        返回: List[int | str]
        """
        return [tile.to_simple_value() for tile in self.hand_tiles]
    
    def get_all_tiles_simple(self) -> List[Union[int, str]]:
        """
        获取所有牌的简单表示（包括鸣牌和手牌）
        
        返回: List[int | str]
        """
        result = []
        
        # 鸣牌
        for group in self.melded_groups:
            result.extend(group.to_simple_tiles())
        
        # 手牌
        result.extend(self.to_simple_hand())
        
        # 胡牌
        if self.winning_tile:
            result.append(self.winning_tile.to_simple_value())
        
        return result


def create_tile_from_value(
    value: Union[int, str],
    is_dora: bool = False,
    is_joker_used: bool = False
) -> Tile:
    """
    快速创建Tile对象
    
    参数：
        value: 牌值
        is_dora: 是否宝牌
        is_joker_used: 是否万用牌代替
    
    返回：
        Tile对象
    """
    joker_type = Tile.infer_joker_type(value) if is_joker_used else None
    return Tile(value, is_dora, is_joker_used, joker_type)
