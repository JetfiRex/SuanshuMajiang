"""
特殊胜利番种检查函数
处理5种特殊番种：八仙过海、四仙过海、天龙、地龙、十三幺
"""

from typing import Optional
from fan_calculator.fan_base import FanResult, FanType
from calculator_base.hand_structure import Hand

# 导入特殊胜利判定器
try:
    from calculator_base.special_winning_checker import SpecialWinningChecker
    SPECIAL_AVAILABLE = True
except ImportError:
    SPECIAL_AVAILABLE = False


def check_ba_xian_guo_hai(hand: Hand) -> Optional[FanResult]:
    """
    八仙过海 (88番)
    
    规则：
    - 8种单张杠（4宝牌 + 4万用牌）
    """
    if not SPECIAL_AVAILABLE:
        return None
    
    checker = SpecialWinningChecker()
    can_win, _ = checker.can_win_ba_xian_guo_hai(hand)
    
    if can_win:
        return FanResult(FanType.BA_XIAN_GUO_HAI)
    
    return None


def check_si_xian_guo_hai(hand: Hand) -> Optional[FanResult]:
    """
    四仙过海 (24番)
    
    规则：
    - 4个宝牌或4个万用牌单张杠
    """
    if not SPECIAL_AVAILABLE:
        return None
    
    checker = SpecialWinningChecker()
    can_win, _ = checker.can_win_si_xian_guo_hai(hand)
    
    if can_win:
        return FanResult(FanType.SI_XIAN_GUO_HAI)
    
    return None


def check_tian_long(hand: Hand) -> Optional[FanResult]:
    """
    天龙 (88番)
    
    规则：
    - 手牌+鸣牌+单张杠中有16个连续的数字（去重后）
    """
    if not SPECIAL_AVAILABLE:
        return None
    
    checker = SpecialWinningChecker()
    can_win, _ = checker.can_win_tian_long(hand)
    
    if can_win:
        return FanResult(FanType.TIAN_LONG)
    
    return None


def check_di_long(hand: Hand) -> Optional[FanResult]:
    """
    地龙 (32番)
    
    规则：
    - 手牌+鸣牌+单张杠中有12项连续的等差数列
    - 公差：1-4，首项<50
    """
    if not SPECIAL_AVAILABLE:
        return None
    
    checker = SpecialWinningChecker()
    can_win, _ = checker.can_win_di_long(hand)
    
    if can_win:
        return FanResult(FanType.DI_LONG)
    
    return None


def check_shi_san_yao(hand: Hand) -> Optional[FanResult]:
    """
    十三幺 (88番)
    
    规则：
    - 必须有 1,9,10,11,19,20,21,49,30,40,+,×,^ 各至少1张
    """
    if not SPECIAL_AVAILABLE:
        return None
    
    checker = SpecialWinningChecker()
    can_win, _ = checker.can_win_shi_san_yao(hand)
    
    if can_win:
        return FanResult(FanType.SHI_SAN_YAO)
    
    return None


def check_all_special_winning_fans(hand: Hand):
    """
    检查所有特殊胜利番种
    
    返回：FanResults对象
    """
    from fan_calculator.fan_base import FanResults
    
    results = FanResults()
    
    # 检查八仙过海
    result = check_ba_xian_guo_hai(hand)
    if result:
        results.add(result)
    
    # 检查四仙过海
    result = check_si_xian_guo_hai(hand)
    if result:
        results.add(result)
    
    # 检查天龙
    result = check_tian_long(hand)
    if result:
        results.add(result)
    
    # 检查地龙
    result = check_di_long(hand)
    if result:
        results.add(result)
    
    # 检查十三幺
    result = check_shi_san_yao(hand)
    if result:
        results.add(result)
    
    return results
