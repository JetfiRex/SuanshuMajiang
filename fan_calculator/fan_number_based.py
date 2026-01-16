"""
算术麻将番数计算 - 基于数字牌的番种
包括：断二、奇一色、全偶数、全一位、全二位、全合数、无合数、全二幂、全多倍、全三倍
"""

from typing import Optional
from calculator_base.hand_structure import Hand
from fan_calculator.fan_base import (
    FanType, FanResult, FanResults,
    get_all_number_tiles, get_all_tiles_for_fan,
    is_prime, is_composite, is_power_of_2
)


def check_duan_er(hand: Hand) -> Optional[FanResult]:
    """
    断二 (6番)
    不出现2的胡牌
    
    规则：只计手牌，不考虑单张杠
    """
    tiles = get_all_tiles_for_fan(hand, include_single_gang=False)
    
    for tile in tiles:
        if tile.value == 2:
            return None
    
    return FanResult(FanType.DUAN_ER)


def check_qi_yi_se(hand: Hand) -> Optional[FanResult]:
    """
    奇一色 (88番)
    在能胡牌的条件下，所有牌都是奇数
    
    规则：
    - 只计手牌，不考虑单张杠
    - 不计断二（在不重复规则中处理）
    """
    numbers = get_all_number_tiles(hand)
    
    # 必须有数字牌
    if not numbers:
        return None
    
    # 检查是否全是奇数
    for num in numbers:
        if num % 2 == 0:
            return None
    
    return FanResult(FanType.QI_YI_SE)


def check_quan_ou_shu(hand: Hand) -> Optional[FanResult]:
    """
    全偶数 (16番)
    牌组中至少一张数字且每个数字都是偶数
    
    规则：只计手牌，不考虑单张杠
    """
    numbers = get_all_number_tiles(hand)
    
    # 必须有数字牌
    if not numbers:
        return None
    
    # 检查是否全是偶数
    for num in numbers:
        if num % 2 != 0:
            return None
    
    return FanResult(FanType.QUAN_OU_SHU)


def check_quan_yi_wei(hand: Hand) -> Optional[FanResult]:
    """
    全一位 (24番)
    有数字牌所有数字均为一位数的胡牌
    
    规则：
    - 只计手牌，不考虑单张杠
    - 一位数指0-9
    """
    numbers = get_all_number_tiles(hand)
    
    # 必须有数字牌
    if not numbers:
        return None
    
    # 检查是否全是一位数
    for num in numbers:
        if num < 0 or num > 9:
            return None
    
    return FanResult(FanType.QUAN_YI_WEI)


def check_quan_er_wei(hand: Hand) -> Optional[FanResult]:
    """
    全二位 (48番)
    有数字牌且所有数字牌均为两位数的胡牌
    
    规则：
    - 只计手牌，不考虑单张杠
    - 两位数指10-99
    """
    numbers = get_all_number_tiles(hand)
    
    # 必须有数字牌
    if not numbers:
        return None
    
    # 检查是否全是两位数
    for num in numbers:
        if num < 10:
            return None
    
    return FanResult(FanType.QUAN_ER_WEI)


def check_quan_he_shu(hand: Hand) -> Optional[FanResult]:
    """
    全合数 (16番)
    有数字牌且数字都是合数
    
    规则：
    - 只计手牌，不考虑单张杠
    - 合数：大于1且不是质数的数
    """
    numbers = get_all_number_tiles(hand)
    
    # 必须有数字牌
    if not numbers:
        return None
    
    # 检查是否全是合数
    for num in numbers:
        if not is_composite(num):
            return None
    
    return FanResult(FanType.QUAN_HE_SHU)


def check_wu_he_shu(hand: Hand) -> Optional[FanResult]:
    """
    无合数 (88番)
    没有合数。数字全是质数或者0, 1以及符号
    
    规则：
    - 此处无视加法大于10的限制
    - 只计手牌，不考虑单张杠
    """
    numbers = get_all_number_tiles(hand)
    
    # 检查是否没有合数
    for num in numbers:
        if is_composite(num):
            return None
    
    return FanResult(FanType.WU_HE_SHU)


def check_quan_er_mi(hand: Hand) -> Optional[FanResult]:
    """
    全二幂 (64番)
    有数字牌且数字都是2的整数幂，包括1
    
    规则：
    - 只计手牌，不考虑单张杠
    - 2的幂：1, 2, 4, 8, 16, 32...
    """
    numbers = get_all_number_tiles(hand)
    
    # 必须有数字牌
    if not numbers:
        return None
    
    # 检查是否全是2的幂
    for num in numbers:
        if not is_power_of_2(num):
            return None
    
    return FanResult(FanType.QUAN_ER_MI)


def check_quan_duo_bei(hand: Hand) -> Optional[FanResult]:
    """
    全多倍 (48番)
    要么牌组没有数字，要么牌组中至少一张数字并且每个数字都是n的倍数，n ≥ 4
    
    规则：
    - 只计手牌，不考虑单张杠
    - 找到最大的公约数n，n必须≥4
    """
    numbers = get_all_number_tiles(hand)
    
    # 如果没有数字牌，符合条件
    if not numbers:
        return FanResult(FanType.QUAN_DUO_BEI, reason="无数字牌")
    
    # 计算最大公约数
    from math import gcd
    from functools import reduce
    
    common_divisor = reduce(gcd, numbers)
    
    # 最大公约数必须≥4
    if common_divisor >= 4:
        return FanResult(FanType.QUAN_DUO_BEI, reason=f"{common_divisor}的倍数")
    
    return None


def check_quan_san_bei(hand: Hand) -> Optional[FanResult]:
    """
    全三倍 (24番)
    牌组中至少一张数字并且每个数字都是3的倍数
    
    规则：只计手牌，不考虑单张杠
    """
    numbers = get_all_number_tiles(hand)
    
    # 必须有数字牌
    if not numbers:
        return None
    
    # 检查是否全是3的倍数
    for num in numbers:
        if num % 3 != 0:
            return None
    
    return FanResult(FanType.QUAN_SAN_BEI)


def check_all_number_based_fans(hand: Hand) -> FanResults:
    """
    检查所有基于数字的番种
    
    参数：
        hand: Hand对象
    
    返回：
        FanResults对象
    """
    results = FanResults()
    
    # 按番值从高到低检查（有些番种是互斥的）
    
    # 88番
    fan = check_qi_yi_se(hand)
    if fan:
        results.add(fan)
    
    fan = check_wu_he_shu(hand)
    if fan:
        results.add(fan)
    
    # 64番
    fan = check_quan_er_mi(hand)
    if fan:
        results.add(fan)
    
    # 48番
    fan = check_quan_er_wei(hand)
    if fan:
        results.add(fan)
    
    fan = check_quan_duo_bei(hand)
    if fan:
        results.add(fan)
    
    # 24番
    fan = check_quan_yi_wei(hand)
    if fan:
        results.add(fan)
    
    fan = check_quan_san_bei(hand)
    if fan:
        results.add(fan)
    
    # 16番
    fan = check_quan_he_shu(hand)
    if fan:
        results.add(fan)
    
    fan = check_quan_ou_shu(hand)
    if fan:
        results.add(fan)
    
    # 6番
    fan = check_duan_er(hand)
    if fan:
        results.add(fan)
    
    return results
