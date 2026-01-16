"""
算术麻将番数计算 - 特殊胡法番种（部分实现）
包括：传统麻将、八小对、连八对
"""

from typing import Optional, List
from calculator_base.hand_structure import Hand, Tile
from fan_calculator.fan_base import FanType, FanResult, FanResults

# 尝试导入传统麻将判定器
try:
    from calculator_base.traditional_mahjong import TraditionalMahjongChecker, EightPairsChecker
    TRADITIONAL_AVAILABLE = True
except ImportError:
    TRADITIONAL_AVAILABLE = False
    print("警告: 未找到 traditional_mahjong.py，传统麻将和八小对功能将不可用")


def check_chuan_tong_majiang(hand: Hand) -> Optional[FanResult]:
    """
    传统麻将 (8番)
    按照牌中间的图案在国标麻将中常规胡牌
    （四组三个加两对，比国标麻将多一对将）
    
    规则：
    - 需要模式1的手牌分组格式
    - 调用传统麻将判定器
    - 遵守"不拆移"原则：只有当win_type明确是"传统麻将"时才计算此番
    """
    if not TRADITIONAL_AVAILABLE:
        return None
    
    # 遵守"不拆移"原则：
    # 如果hand.win_type已经明确指定为"算术麻将"或"八小对"，则不能再计算传统麻将番
    # 只有当win_type是"传统麻将"或None（未指定）时才检查
    if hand.win_type is not None and hand.win_type != "传统麻将":
        return None
    
    # 必须有手牌分组
    if not hand.hand_groups:
        return None
    
    # 构造简单的牌列表（用于传统麻将判定）
    simple_tiles = []
    
    # 收集手牌分组中的牌
    for group in hand.hand_groups:
        for tile in group:
            simple_tiles.append(tile.to_simple_value())
    
    # 收集鸣牌中的牌（不包括单张杠）
    for melded_group in hand.melded_groups:
        if melded_group.group_type != 'single_gang':
            simple_tiles.extend(melded_group.to_simple_tiles())
    
    # 检查是否是传统麻将胡法
    checker = TraditionalMahjongChecker()
    can_win, _ = checker.can_win_traditional(simple_tiles)
    
    if can_win:
        return FanResult(FanType.CHUAN_TONG_MAJIANG)
    
    return None


def check_ba_xiao_dui(hand: Hand) -> Optional[FanResult]:
    """
    八小对 (24番)
    由八个对子（没有式子）组成的门清牌（16张牌）
    
    规则：
    - 对子可以重复
    - 若重复不计暗刻
    - 必须门清（不能有鸣牌，除了单张杠）
    """
    if not TRADITIONAL_AVAILABLE:
        return None
    
    # 检查是否门清（只能有单张杠）
    for melded_group in hand.melded_groups:
        if melded_group.group_type != 'single_gang':
            return None  # 有非单张杠的鸣牌，不是门清
    
    # 必须有手牌分组
    if not hand.hand_groups:
        return None
    
    # 检查是否有8个对子（八小对实际是8对=16张牌）
    if len(hand.hand_groups) != 8:
        return None
    
    # 检查每组是否都是对子（2张相同的牌）
    for group in hand.hand_groups:
        if len(group) != 2:
            return None
        if group[0].value != group[1].value:
            return None
    
    return FanResult(FanType.BA_XIAO_DUI)


def check_lian_ba_dui(hand: Hand) -> Optional[FanResult]:
    """
    连八对 (88番)
    七个对子成等差数列（16张牌）
    
    规则：
    - 必须是7个对子
    - 对子的数值成等差数列
    - 必须门清（不能有鸣牌，除了单张杠）
    """
    # 检查是否门清（只能有单张杠）
    for melded_group in hand.melded_groups:
        if melded_group.group_type != 'single_gang':
            return None  # 有非单张杠的鸣牌，不是门清
    
    # 必须有手牌分组
    if not hand.hand_groups:
        return None
    
    # 检查是否有7个对子（连八对实际是7对=14张牌）
    if len(hand.hand_groups) != 8:
        return None
    
    # 提取每个对子的数值
    pair_values = []
    for group in hand.hand_groups:
        if len(group) != 2:
            return None
        if group[0].value != group[1].value:
            return None
        
        # 必须是数字牌
        if not isinstance(group[0].value, int):
            return None
        
        pair_values.append(group[0].value)
    
    # 排序
    pair_values.sort()
    
    # 检查是否是等差数列
    if len(pair_values) < 2:
        return None
    
    # 计算公差
    diff = pair_values[1] - pair_values[0]
    
    # 验证是否是等差数列
    for i in range(1, len(pair_values)):
        if pair_values[i] - pair_values[i-1] != diff:
            return None
    
    return FanResult(
        FanType.LIAN_BA_DUI,
        reason=f"等差数列，公差={diff}"
    )


def check_all_special_fans(hand: Hand) -> FanResults:
    """
    检查所有特殊胡法番种（部分实现）
    
    参数：
        hand: Hand对象
    
    返回：
        FanResults对象
    """
    results = FanResults()
    
    # 88番
    fan = check_lian_ba_dui(hand)
    if fan:
        results.add(fan)
    
    # 24番
    fan = check_ba_xiao_dui(hand)
    if fan:
        results.add(fan)
    
    # 8番
    fan = check_chuan_tong_majiang(hand)
    if fan:
        results.add(fan)
    
    return results
