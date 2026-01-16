"""
算术麻将番数计算 - 基于算式比较的番种
包括：四同式、三同式、两般高、一般高
"""

from typing import Optional, List, Tuple, Set
from collections import Counter
from calculator_base.hand_structure import Hand, Tile
from calculator_base.parser import PLUS, MULTIPLY, POWER, SYMBOLS
from fan_calculator.fan_base import FanType, FanResult, FanResults


def normalize_formula(tiles: List[Tile]) -> Optional[Tuple]:
    """
    将算式标准化为可比较的形式
    
    对于 a op b = c 形式的算式：
    - 加法和乘法考虑交换律：min(a,b) op max(a,b) = c
    - 次方不考虑交换律：a ∧ b = c
    
    参数：
        tiles: 4张牌的列表
    
    返回：
        标准化的元组 (op, a, b, c) 或 None（如果不是算式）
    """
    if len(tiles) != 4:
        return None
    
    # 找到符号
    op = None
    numbers = []
    
    for tile in tiles:
        if tile.value in SYMBOLS:
            if op is not None:
                return None  # 多个符号，无效
            op = tile.value
        else:
            numbers.append(tile.value)
    
    if op is None or len(numbers) != 3:
        return None  # 不是有效算式
    
    # 根据运算符标准化
    # 需要识别哪个是结果
    # 尝试所有可能的组合
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            k = 3 - i - j  # 第三个数的索引
            
            a, b, c = numbers[i], numbers[j], numbers[k]
            
            # 验证是否满足运算关系
            valid = False
            try:
                if op == PLUS and a + b == c:
                    valid = True
                elif op == MULTIPLY and a * b == c:
                    valid = True
                elif op == POWER and a ** b == c:
                    valid = True
            except (OverflowError, ValueError):
                continue
            
            if valid:
                # 标准化：对于加法和乘法，保证 a <= b
                if op in [PLUS, MULTIPLY]:
                    a, b = min(a, b), max(a, b)
                
                return (op, a, b, c)
    
    return None


def is_formula_group(tiles: List[Tile]) -> bool:
    """判断是否是算式"""
    return normalize_formula(tiles) is not None


def get_all_formulas(hand: Hand) -> List[Tuple]:
    """
    获取手牌中所有算式的标准化表示
    
    参数：
        hand: Hand对象
    
    返回：
        标准化算式列表
    """
    formulas = []
    
    # 从手牌分组中获取
    if hand.hand_groups:
        for group in hand.hand_groups:
            normalized = normalize_formula(group)
            if normalized:
                formulas.append(normalized)
    
    # 从鸣牌中获取（吃牌）
    for melded_group in hand.melded_groups:
        if melded_group.group_type == 'chi':
            normalized = normalize_formula(melded_group.tiles)
            if normalized:
                formulas.append(normalized)
    
    return formulas


def check_si_tong_shi(hand: Hand) -> Optional[FanResult]:
    """
    四同式 (88番)
    拥有四个一样的式子的胡牌
    
    规则：不计四刻子（在不重复规则中处理）
    """
    formulas = get_all_formulas(hand)
    
    if len(formulas) < 4:
        return None
    
    # 统计每个算式出现的次数
    formula_counts = Counter(formulas)
    
    # 检查是否有算式出现4次
    for formula, count in formula_counts.items():
        if count >= 4:
            op, a, b, c = formula
            return FanResult(
                FanType.SI_TONG_SHI,
                reason=f"{a} {op} {b} = {c}"
            )
    
    return None


def check_san_tong_shi(hand: Hand) -> Optional[FanResult]:
    """
    三同式 (48番)
    有三个式子相同的胡牌
    """
    formulas = get_all_formulas(hand)
    
    if len(formulas) < 3:
        return None
    
    # 统计每个算式出现的次数
    formula_counts = Counter(formulas)
    
    # 检查是否有算式出现3次
    for formula, count in formula_counts.items():
        if count >= 3:
            op, a, b, c = formula
            return FanResult(
                FanType.SAN_TONG_SHI,
                reason=f"{a} {op} {b} = {c}"
            )
    
    return None


def check_liang_ban_gao(hand: Hand) -> Optional[FanResult]:
    """
    两般高 (64番)
    有两对式子相同的胡牌
    
    例如：两个 1+9=10 和 两个 2×3=6
    """
    formulas = get_all_formulas(hand)
    
    if len(formulas) < 4:
        return None
    
    # 统计每个算式出现的次数
    formula_counts = Counter(formulas)
    
    # 统计出现至少2次的算式
    pairs = [formula for formula, count in formula_counts.items() if count >= 2]
    
    if len(pairs) >= 2:
        # 格式化原因
        reasons = []
        for formula in pairs[:2]:  # 只显示前两对
            op, a, b, c = formula
            reasons.append(f"{a} {op} {b} = {c}")
        
        return FanResult(
            FanType.LIANG_BAN_GAO,
            reason=" 和 ".join(reasons)
        )
    
    return None


def check_yi_ban_gao(hand: Hand) -> Optional[FanResult]:
    """
    一般高 (8番)
    有一对式子相同的胡牌
    """
    formulas = get_all_formulas(hand)
    
    if len(formulas) < 2:
        return None
    
    # 统计每个算式出现的次数
    formula_counts = Counter(formulas)
    
    # 检查是否有算式出现至少2次
    for formula, count in formula_counts.items():
        if count >= 2:
            op, a, b, c = formula
            return FanResult(
                FanType.YI_BAN_GAO,
                reason=f"{a} {op} {b} = {c}"
            )
    
    return None


def check_all_comparison_fans(hand: Hand) -> FanResults:
    """
    检查所有基于算式比较的番种
    
    参数：
        hand: Hand对象
    
    返回：
        FanResults对象
    """
    results = FanResults()
    
    # 88番
    fan = check_si_tong_shi(hand)
    if fan:
        results.add(fan)
    
    # 64番
    fan = check_liang_ban_gao(hand)
    if fan:
        results.add(fan)
    
    # 48番
    fan = check_san_tong_shi(hand)
    if fan:
        results.add(fan)
    
    # 8番
    fan = check_yi_ban_gao(hand)
    if fan:
        results.add(fan)
    
    return results
