"""
算术麻将番数计算模块

提供完整的番数计算功能，包括44种番型的判断和计算。
"""

from fan_calculator.fan_calculator import (
    FanCalculator,
    calculate_fan,
    get_total_fan,
    can_win_with_fan,
    format_fan_result
)

from fan_calculator.fan_base import (
    FanType,
    FanResult,
    FanResults,
    apply_exclusion_rules
)

__all__ = [
    'FanCalculator',
    'calculate_fan',
    'get_total_fan',
    'can_win_with_fan',
    'format_fan_result',
    'FanType',
    'FanResult',
    'FanResults',
    'apply_exclusion_rules',
]
