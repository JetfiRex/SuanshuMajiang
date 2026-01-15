"""
算术麻将番数计算 - 主计算器
整合所有番种判断，应用不重复规则，计算总番数
"""

from hand_structure import Hand
from fan_calculator.fan_base import FanResults, apply_exclusion_rules
from fan_calculator.fan_number_based import check_all_number_based_fans
from fan_calculator.fan_formula_based import check_all_formula_based_fans
from fan_calculator.fan_tile_info import check_all_tile_info_fans
from fan_calculator.fan_comparison import check_all_comparison_fans
from fan_calculator.fan_special import check_all_special_fans
from fan_calculator.fan_context import check_all_context_fans


class FanCalculator:
    """番数计算器"""
    
    def __init__(self, min_fan=8):
        """
        初始化番数计算器
        
        参数：
            min_fan: 起胡番数（默认8番，新手规则为0番）
        """
        self.min_fan = min_fan
    
    def calculate(self, hand: Hand) -> FanResults:
        """
        计算手牌的番数
        
        参数：
            hand: Hand对象（已经胡牌的手牌）
        
        返回：
            FanResults对象，包含所有番种和总番数
        """
        # 收集所有番种
        all_fans = FanResults()
        
        # 1. 检查基于数字的番种
        number_fans = check_all_number_based_fans(hand)
        for fan in number_fans.results:
            all_fans.add(fan)
        
        # 2. 检查基于算式和刻子的番种
        formula_fans = check_all_formula_based_fans(hand)
        for fan in formula_fans.results:
            all_fans.add(fan)
        
        # 3. 检查基于牌面信息的番种
        tile_info_fans = check_all_tile_info_fans(hand)
        for fan in tile_info_fans.results:
            all_fans.add(fan)
        
        # 4. 检查基于算式比较的番种
        comparison_fans = check_all_comparison_fans(hand)
        for fan in comparison_fans.results:
            all_fans.add(fan)
        
        # 5. 检查特殊胡法番种
        special_fans = check_all_special_fans(hand)
        for fan in special_fans.results:
            all_fans.add(fan)
        
        # 5.5. 检查特殊胜利番种（八仙过海、四仙过海、天龙、地龙、十三幺）
        try:
            from fan_calculator.fan_special_winning import check_all_special_winning_fans
            special_winning_fans = check_all_special_winning_fans(hand)
            for fan in special_winning_fans.results:
                all_fans.add(fan)
        except ImportError:
            pass  # 如果模块不可用，跳过
        
        # 6. 检查需要场上信息的番种
        context_fans = check_all_context_fans(hand)
        for fan in context_fans.results:
            all_fans.add(fan)
        
        # 7. 应用不重复规则
        final_fans = apply_exclusion_rules(all_fans)
        
        # 8. 检查无番胡
        # 如果没有任何番种，则为无番胡（8番）
        if len(final_fans.results) == 0:
            from fan_calculator.fan_base import FanType, FanResult
            final_fans.add(FanResult(FanType.WU_FAN_HU))
        
        # 9. 按番值排序
        final_fans.sort_by_value()
        
        return final_fans
    
    def can_win(self, hand: Hand) -> bool:
        """
        判断是否满足起胡条件
        
        参数：
            hand: Hand对象
        
        返回：
            是否可以胡牌（番数 >= min_fan）
        """
        result = self.calculate(hand)
        return result.get_total_fan() >= self.min_fan
    
    def format_result(self, fan_results: FanResults, verbose: bool = False) -> str:
        """
        格式化番数结果
        
        参数：
            fan_results: FanResults对象
            verbose: 是否显示详细信息（包括被排除的番种）
        
        返回：
            格式化的字符串
        """
        lines = []
        
        # 总番数
        total = fan_results.get_total_fan()
        lines.append("=" * 60)
        lines.append(f"总计: {total}番")
        lines.append("=" * 60)
        
        # 番种列表
        if fan_results.results:
            lines.append("")
            lines.append("番种明细:")
            lines.append("-" * 60)
            for result in fan_results.results:
                lines.append(f"  {result}")
        else:
            lines.append("")
            lines.append("无番胡（需要额外判定）")
        
        # 被排除的番种（详细模式）
        if verbose and fan_results.excluded:
            lines.append("")
            lines.append("被排除的番种:")
            lines.append("-" * 60)
            for fan_type, reason in fan_results.excluded:
                lines.append(f"  {fan_type.fan_name}: {reason}")
        
        # 起胡判断
        lines.append("")
        lines.append("=" * 60)
        if total >= self.min_fan:
            lines.append(f"✅ 满足起胡条件（{self.min_fan}番起胡）")
        else:
            lines.append(f"❌ 不满足起胡条件（需要{self.min_fan}番，当前{total}番）")
        lines.append("=" * 60)
        
        return "\n".join(lines)


# 便捷函数

def calculate_fan(hand: Hand, min_fan: int = 8) -> FanResults:
    """
    便捷函数：计算番数
    
    参数：
        hand: Hand对象
        min_fan: 起胡番数（默认8，新手规则为0）
    
    返回：
        FanResults对象
    """
    calculator = FanCalculator(min_fan=min_fan)
    return calculator.calculate(hand)


def get_total_fan(hand: Hand, min_fan: int = 8) -> int:
    """
    便捷函数：获取总番数
    
    参数：
        hand: Hand对象
        min_fan: 起胡番数（默认8，新手规则为0）
    
    返回：
        总番数
    """
    result = calculate_fan(hand, min_fan)
    return result.get_total_fan()


def can_win_with_fan(hand: Hand, min_fan: int = 8) -> tuple[bool, int]:
    """
    便捷函数：判断是否可以胡牌及番数
    
    参数：
        hand: Hand对象
        min_fan: 起胡番数（默认8，新手规则为0）
    
    返回：
        (是否可以胡牌, 总番数)
    """
    calculator = FanCalculator(min_fan=min_fan)
    result = calculator.calculate(hand)
    total = result.get_total_fan()
    return total >= calculator.min_fan, total


def format_fan_result(hand: Hand, verbose: bool = False, min_fan: int = 8) -> str:
    """
    便捷函数：格式化输出番数结果
    
    参数：
        hand: Hand对象
        verbose: 是否显示详细信息
        min_fan: 起胡番数（默认8，新手规则为0）
    
    返回：
        格式化的字符串
    """
    calculator = FanCalculator(min_fan=min_fan)
    result = calculator.calculate(hand)
    return calculator.format_result(result, verbose)
