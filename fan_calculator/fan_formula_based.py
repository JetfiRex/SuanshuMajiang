"""
算术麻将番数计算 - 基于算式和刻子的番种
包括：大三元、小三元、四刻子、三刻子、大四喜、小四喜、
      加一色、乘一色、次一色、四门齐、次方
"""

from typing import Optional, List, Tuple
from collections import Counter
from calculator_base.hand_structure import Hand, Tile
from calculator_base.parser import PLUS, MULTIPLY, POWER, SYMBOLS
from fan_calculator.fan_base import (
    FanType, FanResult, FanResults,
    get_all_tiles_for_fan
)


def is_formula_group(tiles: List[Tile]) -> bool:
    """
    判断一组牌是否是算式（4张牌，包含符号）
    
    参数：
        tiles: 牌组
    
    返回：
        是否是算式
    """
    if len(tiles) != 4:
        return False
    
    symbol_count = sum(1 for t in tiles if t.value in SYMBOLS)
    return symbol_count == 1


def is_kezi_group(tiles: List[Tile]) -> bool:
    """
    判断一组牌是否是刻子（4张相同的牌）
    
    参数：
        tiles: 牌组
    
    返回：
        是否是刻子
    """
    if len(tiles) != 4:
        return False
    
    values = [t.value for t in tiles]
    return len(set(values)) == 1


def get_formula_operator(tiles: List[Tile]) -> Optional[str]:
    """
    获取算式的运算符
    
    参数：
        tiles: 算式牌组
    
    返回：
        运算符（+, ×, ∧）或None
    """
    for tile in tiles:
        if tile.value in SYMBOLS:
            return tile.value
    return None


def count_formulas_by_operator(hand: Hand) -> Tuple[int, int, int]:
    """
    统计各类算式的数量
    
    参数：
        hand: Hand对象
    
    返回：
        (加法数量, 乘法数量, 次方数量)
    """
    plus_count = 0
    multiply_count = 0
    power_count = 0
    
    # 从手牌分组中统计
    if hand.hand_groups:
        for group in hand.hand_groups:
            if is_formula_group(group):
                op = get_formula_operator(group)
                if op == PLUS:
                    plus_count += 1
                elif op == MULTIPLY:
                    multiply_count += 1
                elif op == POWER:
                    power_count += 1
    
    # 从鸣牌中统计（吃牌也是算式）
    for melded_group in hand.melded_groups:
        if melded_group.group_type == 'chi':
            tiles = melded_group.tiles
            if is_formula_group(tiles):
                op = get_formula_operator(tiles)
                if op == PLUS:
                    plus_count += 1
                elif op == MULTIPLY:
                    multiply_count += 1
                elif op == POWER:
                    power_count += 1
    
    return plus_count, multiply_count, power_count


def count_kezi(hand: Hand) -> int:
    """
    统计刻子数量（不考虑单张杠）
    
    参数：
        hand: Hand对象
    
    返回：
        刻子数量
    """
    kezi_count = 0
    
    # 从手牌分组中统计
    if hand.hand_groups:
        for group in hand.hand_groups:
            if is_kezi_group(group):
                kezi_count += 1
    
    # 从鸣牌中统计（碰牌是刻子）
    for melded_group in hand.melded_groups:
        if melded_group.group_type == 'peng':
            kezi_count += 1
    
    return kezi_count


def count_symbol_tiles(hand: Hand, include_single_gang: bool = True) -> int:
    """
    统计符号牌总张数
    
    参数：
        hand: Hand对象
        include_single_gang: 是否包括单张杠的符号牌
    
    返回：
        符号牌总张数
    """
    tiles = get_all_tiles_for_fan(hand, include_single_gang=include_single_gang)
    return sum(1 for t in tiles if t.value in SYMBOLS)


def count_multiples_of_10(hand: Hand) -> int:
    """
    统计10的倍数的张数
    
    参数：
        hand: Hand对象
    
    返回：
        10的倍数的张数
    """
    tiles = get_all_tiles_for_fan(hand, include_single_gang=False)
    return sum(1 for t in tiles if isinstance(t.value, int) and t.value % 10 == 0)


# ============================================================
# 符号相关番种
# ============================================================

def check_da_san_yuan(hand: Hand) -> Optional[FanResult]:
    """
    大三元 (88番)
    拥有三个符号的刻子
    
    规则：不计三刻子（在不重复规则中处理）
    """
    symbol_kezis = []
    
    # 检查手牌分组中的刻子
    if hand.hand_groups:
        for group in hand.hand_groups:
            if is_kezi_group(group) and group[0].value in SYMBOLS:
                symbol_kezis.append(group[0].value)
    
    # 检查鸣牌中的碰牌
    for melded_group in hand.melded_groups:
        if melded_group.group_type == 'peng':
            if melded_group.tiles[0].value in SYMBOLS:
                symbol_kezis.append(melded_group.tiles[0].value)
    
    # 检查是否有三个不同的符号刻子
    unique_symbols = set(symbol_kezis)
    if len(unique_symbols) >= 3:
        return FanResult(FanType.DA_SAN_YUAN)
    
    return None


def check_xiao_san_yuan(hand: Hand) -> Optional[FanResult]:
    """
    小三元 (32番)
    符号牌共计至少8张（单张杠的符号万用牌计算）
    
    规则：只计手牌，但单张杠的符号万用牌也算
    """
    count = count_symbol_tiles(hand, include_single_gang=True)
    
    if count >= 8:
        return FanResult(FanType.XIAO_SAN_YUAN)
    
    return None


# ============================================================
# 刻子相关番种
# ============================================================

def check_si_ke_zi(hand: Hand) -> Optional[FanResult]:
    """
    四刻子 (88番)
    拥有四个刻子的胡牌
    
    规则：
    - 不考虑单张杠
    - 不计四刻子（在不重复规则中处理）
    """
    kezi_count = count_kezi(hand)
    
    if kezi_count >= 4:
        return FanResult(FanType.SI_KE_ZI)
    
    return None


def check_san_ke_zi(hand: Hand) -> Optional[FanResult]:
    """
    三刻子 (48番)
    拥有三个刻子的胡牌
    
    规则：
    - 不考虑单张杠
    - 不计单个刻子（在不重复规则中处理）
    """
    kezi_count = count_kezi(hand)
    
    if kezi_count >= 3:
        return FanResult(FanType.SAN_KE_ZI)
    
    return None


# ============================================================
# 四喜相关番种
# ============================================================

def check_da_si_xi(hand: Hand) -> Optional[FanResult]:
    """
    大四喜 (88番)
    牌组中至少9个10的倍数
    
    注意：规则中说"四喜有五个"，这里理解为至少9个10的倍数
    """
    count = count_multiples_of_10(hand)
    
    if count >= 9:
        return FanResult(FanType.DA_SI_XI)
    
    return None


def check_xiao_si_xi(hand: Hand) -> Optional[FanResult]:
    """
    小四喜 (32番)
    拥有至少6张10的倍数的胡牌
    """
    count = count_multiples_of_10(hand)
    
    if count >= 6:
        return FanResult(FanType.XIAO_SI_XI)
    
    return None


# ============================================================
# 一色相关番种
# ============================================================

def check_jia_yi_se(hand: Hand) -> Optional[FanResult]:
    """
    加一色 (12番)
    四个式子，只有加法
    
    规则：不计断二（在不重复规则中处理）
    """
    plus_count, multiply_count, power_count = count_formulas_by_operator(hand)
    
    # 必须恰好4个加法，0个乘法和次方
    if plus_count == 4 and multiply_count == 0 and power_count == 0:
        return FanResult(FanType.JIA_YI_SE)
    
    return None


def check_cheng_yi_se(hand: Hand) -> Optional[FanResult]:
    """
    乘一色 (12番)
    四个式子，只有乘法
    """
    plus_count, multiply_count, power_count = count_formulas_by_operator(hand)
    
    # 必须恰好4个乘法，0个加法和次方
    if plus_count == 0 and multiply_count == 4 and power_count == 0:
        return FanResult(FanType.CHENG_YI_SE)
    
    return None


def check_ci_yi_se(hand: Hand) -> Optional[FanResult]:
    """
    次一色 (64番)
    四个式子，只有次方
    
    规则：不计次方（在不重复规则中处理）
    """
    plus_count, multiply_count, power_count = count_formulas_by_operator(hand)
    
    # 必须恰好4个次方，0个加法和乘法
    if plus_count == 0 and multiply_count == 0 and power_count == 4:
        return FanResult(FanType.CI_YI_SE)
    
    return None


# ============================================================
# 其他番种
# ============================================================

def check_si_men_qi(hand: Hand) -> Optional[FanResult]:
    """
    四门齐 (12番)
    由一个刻子，一个加法，一个乘法，一个次方组成的胡牌
    
    规则：不计刻子和次方本身
    """
    plus_count, multiply_count, power_count = count_formulas_by_operator(hand)
    kezi_count = count_kezi(hand)
    
    # 必须恰好1个刻子，1个加法，1个乘法，1个次方
    if kezi_count == 1 and plus_count == 1 and multiply_count == 1 and power_count == 1:
        return FanResult(FanType.SI_MEN_QI)
    
    return None


def check_ci_fang(hand: Hand) -> Optional[FanResult]:
    """
    次方 (2番)
    胡牌时每一个出现次方的算式计一次
    
    规则：可以叠加，有n个次方就计n次
    """
    plus_count, multiply_count, power_count = count_formulas_by_operator(hand)
    
    if power_count > 0:
        return FanResult(FanType.CI_FANG, count=power_count)
    
    return None


def check_all_formula_based_fans(hand: Hand) -> FanResults:
    """
    检查所有基于算式和刻子的番种
    
    参数：
        hand: Hand对象
    
    返回：
        FanResults对象
    """
    results = FanResults()
    
    # 88番
    fan = check_da_san_yuan(hand)
    if fan:
        results.add(fan)
    
    fan = check_si_ke_zi(hand)
    if fan:
        results.add(fan)
    
    fan = check_da_si_xi(hand)
    if fan:
        results.add(fan)
    
    # 64番
    fan = check_ci_yi_se(hand)
    if fan:
        results.add(fan)
    
    # 48番
    fan = check_san_ke_zi(hand)
    if fan:
        results.add(fan)
    
    # 32番
    fan = check_xiao_san_yuan(hand)
    if fan:
        results.add(fan)
    
    fan = check_xiao_si_xi(hand)
    if fan:
        results.add(fan)
    
    # 12番
    fan = check_jia_yi_se(hand)
    if fan:
        results.add(fan)
    
    fan = check_cheng_yi_se(hand)
    if fan:
        results.add(fan)
    
    fan = check_si_men_qi(hand)
    if fan:
        results.add(fan)
    
    # 2番
    fan = check_ci_fang(hand)
    if fan:
        results.add(fan)
    
    return results
