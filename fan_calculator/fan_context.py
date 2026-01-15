"""
算术麻将番数计算 - 需要场上信息的番种
包括：门清、不求人、全求人、杠上开花、抢杠、海底捞月、听符号、天胡、暗刻、明刻、杠
"""

from typing import Optional
from hand_structure import Hand, MeldedGroup
from parser import SYMBOLS
from fan_calculator.fan_base import FanType, FanResult, FanResults
from fan_calculator.fan_formula_based import is_kezi_group


# ============================================================
# 可直接从牌面判断的番种
# ============================================================

def check_men_qing(hand: Hand) -> Optional[FanResult]:
    """
    门清 (2番)
    无吃碰明杠（没有chi、peng、gang_ming类型的鸣牌）
    
    规则：
    - 单张杠（single_gang）和暗杠（gang_an）不影响门清
    """
    for melded_group in hand.melded_groups:
        if melded_group.group_type in ['chi', 'peng', 'gang_ming']:
            return None
    
    return FanResult(FanType.MEN_QING)


def check_ming_ke(hand: Hand) -> Optional[FanResult]:
    """
    明刻 (2番)
    明刻指的是鸣牌中的碰（括号里的刻子）
    
    规则：
    - 每一个明刻算一次
    - 可以叠加
    """
    ming_ke_count = 0
    
    for melded_group in hand.melded_groups:
        if melded_group.group_type == 'peng':
            ming_ke_count += 1
    
    if ming_ke_count > 0:
        return FanResult(FanType.MING_KE, count=ming_ke_count)
    
    return None


def check_an_ke(hand: Hand) -> Optional[FanResult]:
    """
    暗刻 (4番)
    暗刻指的是手牌分组中的刻子（不在括号里）
    
    规则：
    - 每一个暗刻算一次
    - 可以叠加
    """
    an_ke_count = 0
    
    # 检查手牌分组中的刻子
    if hand.hand_groups:
        for group in hand.hand_groups:
            if is_kezi_group(group):
                an_ke_count += 1
    
    if an_ke_count > 0:
        return FanResult(FanType.AN_KE, count=an_ke_count)
    
    return None


def check_gang(hand: Hand) -> Optional[FanResult]:
    """
    杠 (4番)
    统计杠牌数量（明杠和暗杠）
    
    规则：
    - 每一个杠算一次
    - 可以叠加
    - 不包括单张杠
    """
    gang_count = 0
    
    for melded_group in hand.melded_groups:
        if melded_group.group_type in ['gang_ming', 'gang_an']:
            gang_count += 1
    
    if gang_count > 0:
        return FanResult(FanType.GANG, count=gang_count)
    
    return None


def check_ting_fu_hao(hand: Hand) -> Optional[FanResult]:
    """
    听符号 (2番)
    听符号且用符号胡
    
    规则：
    - 胡牌必须是符号牌
    """
    if hand.winning_tile and hand.winning_tile.value in SYMBOLS:
        return FanResult(FanType.TING_FU_HAO, reason=hand.winning_tile.value)
    
    return None


def check_quan_qiu_ren(hand: Hand) -> Optional[FanResult]:
    """
    全求人 (4番)
    三组鸣牌（吃/碰/明杠） + 不自摸（点胡）
    
    规则：
    - 必须有3组鸣牌（chi、peng、gang_ming）
    - 必须是点胡（winning_method != '自摸'）
    """
    # 统计鸣牌数量（吃/碰/明杠）
    melded_count = 0
    
    for melded_group in hand.melded_groups:
        if melded_group.group_type in ['chi', 'peng', 'gang_ming']:
            melded_count += 1
    
    # 检查条件：至少3组鸣牌 + 不自摸
    if melded_count >= 3:
        # 检查是否点胡（不是自摸）
        if hand.winning_method and hand.winning_method != '自摸':
            return FanResult(FanType.QUAN_QIU_REN)
        # 如果没有winning_method，也可能是点胡，但需要明确标记
        # 这里保守处理，只在有明确winning_method且不是自摸时才算
    
    return None


# ============================================================
# 需要winning_method的番种
# ============================================================

def check_bu_qiu_ren(hand: Hand) -> Optional[FanResult]:
    """
    不求人 (6番)
    门清 + 自摸
    
    规则：
    - 必须门清（无吃碰明杠）
    - 必须自摸
    - 不计门清（在不重复规则中处理）
    """
    # 检查是否门清
    if not check_men_qing(hand):
        return None
    
    # 检查是否自摸
    if hand.winning_method == '自摸':
        return FanResult(FanType.BU_QIU_REN)
    
    return None


def check_gang_shang_kai_hua(hand: Hand) -> Optional[FanResult]:
    """
    杠上开花 (8番)
    杠后摸牌胡
    
    规则：
    - winning_method == '杠上开花'
    """
    if hand.winning_method == '杠上开花':
        return FanResult(FanType.GANG_SHANG_KAI_HUA)
    
    return None


def check_qiang_gang(hand: Hand) -> Optional[FanResult]:
    """
    抢杠 (8番)
    抢杠胡牌
    
    规则：
    - winning_method == '抢杠'
    """
    if hand.winning_method == '抢杠':
        return FanResult(FanType.QIANG_GANG)
    
    return None


def check_hai_di_lao_yue(hand: Hand) -> Optional[FanResult]:
    """
    海底捞月 (16番)
    最后一张牌胡
    
    规则：
    - winning_method == '海底捞月'
    """
    if hand.winning_method == '海底捞月':
        return FanResult(FanType.HAI_DI_LAO_YUE)
    
    return None


def check_tian_hu(hand: Hand) -> Optional[FanResult]:
    """
    天胡 (32番)
    起手听牌（第一轮就胡）
    
    规则：
    - winning_method == '天胡'
    """
    if hand.winning_method == '天胡':
        return FanResult(FanType.TIAN_HU)
    
    return None


def check_all_context_fans(hand: Hand) -> FanResults:
    """
    检查所有需要场上信息的番种
    
    参数：
        hand: Hand对象
    
    返回：
        FanResults对象
    """
    results = FanResults()
    
    # 32番
    fan = check_tian_hu(hand)
    if fan:
        results.add(fan)
    
    # 16番
    fan = check_hai_di_lao_yue(hand)
    if fan:
        results.add(fan)
    
    # 8番
    fan = check_gang_shang_kai_hua(hand)
    if fan:
        results.add(fan)
    
    fan = check_qiang_gang(hand)
    if fan:
        results.add(fan)
    
    # 6番
    fan = check_bu_qiu_ren(hand)
    if fan:
        results.add(fan)
    
    # 4番
    fan = check_quan_qiu_ren(hand)
    if fan:
        results.add(fan)
    
    fan = check_an_ke(hand)
    if fan:
        results.add(fan)
    
    fan = check_gang(hand)
    if fan:
        results.add(fan)
    
    # 2番
    fan = check_men_qing(hand)
    if fan:
        results.add(fan)
    
    fan = check_ming_ke(hand)
    if fan:
        results.add(fan)
    
    fan = check_ting_fu_hao(hand)
    if fan:
        results.add(fan)
    
    return results
