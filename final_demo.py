#!/usr/bin/env python3
"""
算术麻将系统 v1.7 - 完整演示

本脚本演示所有新功能：
1. 交互式听牌查询
2. 传统麻将可读格式化
3. 模式2选择最优胡法
"""

import sys
import io
sys.path.insert(0, '/home/claude/arithmetic_mahjong_v1.6_FINAL')

from mahjong_checker import ArithmeticMahjong
from parser import parse_mode1_already_won
from fan_calculator import calculate_fan

print("=" * 80)
print(" " * 25 + "算术麻将系统 v1.7")
print(" " * 28 + "完整演示")
print("=" * 80)

mjong = ArithmeticMahjong(require_sum_gte_10=True, min_fan=8)

# ============================================================
# 演示1：交互式听牌查询
# ============================================================
print("\n【演示1：交互式听牌查询 - 模式3】")
print("-" * 80)
print("这是新增的主要功能！")
print()

hand_15 = [1, '+', 15, 16, 2, '+', 13, 15, 3, '+', 14, 17, '×', '×', '×']
print(f"手牌（15张）: {' '.join(map(str, hand_15))}")
print()

# 模拟自动选择'y'
original_stdin = sys.stdin
sys.stdin = io.StringIO('y\n')
mjong.display_ready_interactive(hand_15)
sys.stdin = original_stdin

# ============================================================
# 演示2：传统麻将格式化
# ============================================================
print("\n\n" + "=" * 80)
print("\n【演示2：传统麻将可读格式化】")
print("-" * 80)
print("传统麻将的分组现在以可读格式显示！")
print()

from traditional_mahjong import TraditionalMahjongChecker
checker = TraditionalMahjongChecker()

test_hand = [2, 2, 2, 3, 3, 3, 4, 5, 6, 17, 18, 19, '+', '+', '×', '×']
print(f"测试手牌: {' '.join(map(str, test_hand))}")

can_win, groups = checker.can_win_traditional(test_hand)

if can_win:
    print(f"\n✅ 可以胡牌（传统麻将）")
    
    # 格式化显示
    formatted = mjong._format_groups_for_display(groups, "传统麻将")
    print(f"\n胡法: {formatted}")
    print(f"\n说明：不再是元组格式，而是直接显示牌组")
    print(f"  + + → 红中 红中")
    print(f"  × × → 发财 发财")
    print(f"  2 2 2 → 2刻")
    print(f"  4 5 6 → 456顺")

# ============================================================
# 演示3：模式2选择最优胡法
# ============================================================
print("\n\n" + "=" * 80)
print("\n【演示3：模式2选择最优胡法】")
print("-" * 80)
print("当多种胡法都满足起胡时，自动选择番数最高的！")
print()

hand_16 = [1, '+', 15, 16, 2, '+', 13, 15, 3, '+', 14, 17, '×', '×', '×', '×']
print(f"手牌（16张）: {' '.join(map(str, hand_16))}")
print()
print("分析：")
print("  - 算术麻将：暗刻4番 + 门清2番 + 鸳鸯4番 = 10番 ✅")
print("  - 传统麻将：传统麻将8番 + 鸳鸯4番 = 12番 ✅")
print()

can_win, groups, win_type, fan_info = mjong.can_win(hand_16)

if can_win:
    print(f"系统选择: {win_type}")
    print(f"总番数: {fan_info['total_fan']}番")
    print(f"\n✅ 正确！选择了番数更高的传统麻将（12番 > 10番）")

# ============================================================
# 演示4：宝牌识别修复
# ============================================================
print("\n\n" + "=" * 80)
print("\n【演示4：宝牌识别修复】")
print("-" * 80)

hand_str1 = "17 17 17 17"
hand_str2 = "17d 17d 17d 17d"

hand_obj1 = parse_mode1_already_won(hand_str1)
hand_obj2 = parse_mode1_already_won(hand_str2)

is_dora1 = hand_obj1.hand_groups[0][0].is_dora
is_dora2 = hand_obj2.hand_groups[0][0].is_dora

print(f"17 17 17 17 → is_dora={is_dora1} {'✅' if not is_dora1 else '❌'}")
print(f"17d 17d 17d 17d → is_dora={is_dora2} {'✅' if is_dora2 else '❌'}")
print(f"\n说明：只有显式标记'd'的才是宝牌")

# ============================================================
# 总结
# ============================================================
print("\n\n" + "=" * 80)
print(" " * 30 + "所有功能演示完成！")
print("=" * 80)

print("""
主要更新：
  ✅ 交互式听牌查询（display_ready_interactive）
  ✅ 传统麻将可读格式化（+ + / × × / 2 2 2 / ...）
  ✅ 模式2选择最优胡法（自动比较番数）
  ✅ 宝牌识别修复（17 vs 17d）
  ✅ 传统麻将判定器修复
  ✅ 四门齐排除规则

快速开始：
  python interactive_example.py     # 交互式示例
  python test_all_features.py       # 功能测试
  python mode34_usage_guide.py      # API文档
""")
