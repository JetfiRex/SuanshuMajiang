"""
空听判断模块
用于判断听牌是否为空听（牌库中已无此牌）
"""

from collections import Counter
from calculator_base.parser import SYMBOLS, JOKERS, JOKER_TIAO, JOKER_TONG, JOKER_WAN, JOKER_SYMBOL


# 牌库配置（每种牌的数量）
TILE_POOL = {
    # 数字牌 0-21: 每张2张
    **{i: 2 for i in range(22)},
    
    # 万字牌 24,25,27,28,30,32,35,36,40,49: 每张2张
    24: 2, 25: 2, 27: 2, 28: 2, 30: 2,
    32: 2, 35: 2, 36: 2, 40: 2, 49: 2,
    
    # 符号牌: 每张4张（因为有多个算式需要）
    '+': 4,
    '×': 4,
    '∧': 4,
    
    # 万用牌: 每种1张
    JOKER_TIAO: 1,    # 条子万用（0-9）
    JOKER_TONG: 1,    # 筒子万用（10-19）
    JOKER_WAN: 1,     # 万字万用（20-49）
    JOKER_SYMBOL: 1,  # 符号万用
}


def get_joker_for_tile(tile):
    """
    获取某张牌对应的万用牌类型
    
    参数：
        tile: 牌值
    
    返回：
        对应的万用牌类型，如果没有则返回None
    """
    if isinstance(tile, int):
        if 0 <= tile <= 9:
            return JOKER_TIAO
        elif 10 <= tile <= 19:
            return JOKER_TONG
        elif 20 <= tile <= 49:
            return JOKER_WAN
    elif tile in SYMBOLS:
        return JOKER_SYMBOL
    return None


def count_tiles_used(hand_tiles):
    """
    统计手牌中每张牌的使用次数
    
    参数：
        hand_tiles: 手牌列表（包括鸣牌）
    
    返回：
        Counter对象，记录每张牌的使用次数
    """
    return Counter(hand_tiles)


def check_tile_availability(tile, tiles_used):
    """
    检查某张牌的可用性
    
    参数：
        tile: 要检查的牌
        tiles_used: Counter对象，记录已使用的牌
    
    返回：
        (status, joker_type)
        status: 'available' | 'need_joker' | 'empty'
        joker_type: 如果需要万用牌，返回万用牌类型；否则返回None
    """
    # 获取牌库中此牌的总数
    total_in_pool = TILE_POOL.get(tile, 0)
    
    if total_in_pool == 0:
        # 牌库中没有这张牌，只能用万用牌
        joker_type = get_joker_for_tile(tile)
        if joker_type is None:
            return 'empty', None
        
        # 检查对应的万用牌是否还有
        joker_used = tiles_used.get(joker_type, 0)
        joker_total = TILE_POOL.get(joker_type, 0)
        
        if joker_used < joker_total:
            return 'need_joker', joker_type
        else:
            return 'empty', None
    
    # 牌库中有这张牌
    used = tiles_used.get(tile, 0)
    
    if used < total_in_pool:
        # 还有普通牌可用
        return 'available', None
    else:
        # 普通牌用完了，检查万用牌
        joker_type = get_joker_for_tile(tile)
        if joker_type is None:
            return 'empty', None
        
        joker_used = tiles_used.get(joker_type, 0)
        joker_total = TILE_POOL.get(joker_type, 0)
        
        if joker_used < joker_total:
            return 'need_joker', joker_type
        else:
            return 'empty', None


def analyze_ready_tiles(ready_tiles, hand_tiles):
    """
    分析听牌的可用性
    
    参数：
        ready_tiles: 听牌列表
        hand_tiles: 手牌列表（包括鸣牌）
    
    返回：
        dict: {
            tile: {
                'status': 'available' | 'need_joker' | 'empty',
                'joker_type': 万用牌类型（如果需要）,
                'display': 显示文本
            }
        }
    """
    tiles_used = count_tiles_used(hand_tiles)
    result = {}
    
    for tile in ready_tiles:
        status, joker_type = check_tile_availability(tile, tiles_used)
        
        if status == 'available':
            display = str(tile)
        elif status == 'need_joker':
            joker_name = get_joker_name(joker_type)
            display = f"{tile}（需要{joker_name}）"
        else:  # empty
            display = f"{tile}（空听）"
        
        result[tile] = {
            'status': status,
            'joker_type': joker_type,
            'display': display
        }
    
    return result


def get_joker_name(joker_type):
    """获取万用牌的显示名称"""
    if joker_type == JOKER_TIAO:
        return "条子万用"
    elif joker_type == JOKER_TONG:
        return "筒子万用"
    elif joker_type == JOKER_WAN:
        return "万字万用"
    elif joker_type == JOKER_SYMBOL:
        return "符号万用"
    else:
        return "万用牌"


def format_ready_tiles_with_status(ready_analysis):
    """
    格式化听牌分析结果
    
    参数：
        ready_analysis: analyze_ready_tiles的返回值
    
    返回：
        格式化的字符串列表
    """
    lines = []
    
    # 分组：正常听牌、需要万用、空听
    available = []
    need_joker = []
    empty = []
    
    for tile, info in ready_analysis.items():
        if info['status'] == 'available':
            available.append(info['display'])
        elif info['status'] == 'need_joker':
            need_joker.append(info['display'])
        else:
            empty.append(info['display'])
    
    if available:
        lines.append(f"  正常听牌: {', '.join(available)}")
    if need_joker:
        lines.append(f"  需要万用: {', '.join(need_joker)}")
    if empty:
        lines.append(f"  空听: {', '.join(empty)}")
    
    return lines


if __name__ == "__main__":
    # 测试用例1：(19d)(1 + 18 19)(2 + 8 10)(3 + 7 10)10 + 9
    print("测试用例1: (19d)(1 + 18 19)(2 + 8 10)(3 + 7 10)10 + 9")
    hand1 = [19, 1, '+', 18, 19, 2, '+', 8, 10, 3, '+', 7, 10, 10, '+', 9]
    ready1 = [19, 1]  # 理论上听19和1
    
    tiles_used1 = count_tiles_used(hand1)
    print(f"手牌: {hand1}")
    print(f"使用统计: {dict(tiles_used1)}")
    print(f"听牌: {ready1}")
    
    analysis1 = analyze_ready_tiles(ready1, hand1)
    for tile, info in analysis1.items():
        print(f"  {tile}: {info['display']} (status={info['status']})")
    print()
    
    # 测试用例2：(19d)(1 + 18 19)(2 + 8 10w)(3 + 7 10)10 + 9
    print("测试用例2: (19d)(1 + 18 19)(2 + 8 10w)(3 + 7 10)10 + 9")
    hand2 = [19, 1, '+', 18, 19, 2, '+', 8, JOKER_TONG, 3, '+', 7, 10, 10, '+', 9]
    ready2 = [19, 1]
    
    tiles_used2 = count_tiles_used(hand2)
    print(f"手牌: {hand2}")
    print(f"使用统计: {dict(tiles_used2)}")
    print(f"听牌: {ready2}")
    
    analysis2 = analyze_ready_tiles(ready2, hand2)
    for tile, info in analysis2.items():
        print(f"  {tile}: {info['display']} (status={info['status']})")
    print()
    
    print("格式化输出:")
    print("\n".join(format_ready_tiles_with_status(analysis2)))
