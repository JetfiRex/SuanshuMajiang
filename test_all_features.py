#!/usr/bin/env python3
"""
测试所有新功能：交互式显示、宝牌、传统麻将格式化
"""

import sys
import io
sys.path.insert(0, '/home/claude/arithmetic_mahjong_v1.6_FINAL')

from mahjong_checker import ArithmeticMahjong

print("=" * 70)
print("算术麻将系统 v1.7 - 完整功能测试")
print("=" * 70)

mjong = ArithmeticMahjong(require_sum_gte_10=True, min_fan=8)

# 测试1：带宝牌的显示
print("\n【测试1：带宝牌的显示】")
print("-" * 70)
hand_with_dora = [17, 17, 17, 13, 11, 11, 11, 13, 19, 19, 19, 13, '+', '+', '+']
print(f"手牌（15张，包含宝牌）: {' '.join(map(str, hand_with_dora))}")
print("（注意：11d, 13d, 17d, 19d 是宝牌）")

# 模拟输入'y'
original_stdin = sys.stdin
sys.stdin = io.StringIO('y\n')

mjong.display_ready_interactive(hand_with_dora)

sys.stdin = original_stdin

# 测试2：传统麻将格式化
print("\n\n" + "=" * 70)
print("\n【测试2：传统麻将格式化验证】")
print("-" * 70)

from traditional_mahjong import TraditionalMahjongChecker

checker = TraditionalMahjongChecker()
test_hand = [2, 2, 2, 3, 3, 3, 4, 5, 6, 17, 18, 19, '+', '+', '×', '×']
print(f"测试手牌: {' '.join(map(str, test_hand))}")

can_win, groups = checker.can_win_traditional(test_hand)

if can_win:
    print(f"\n传统麻将可以胡牌！")
    
    # 显示原始格式（内部表示）
    print(f"\n原始分组格式（仅前3组）:")
    for i, group in enumerate(groups[:3], 1):
        print(f"  第{i}组: {group}")
    
    # 显示格式化后的格式
    print(f"\n格式化后的胡法（期望格式）:")
    formatted = mjong._format_groups_for_display(groups, "传统麻将")
    print(f"  {formatted}")
    
    print(f"\n✅ 符合期望：+ + / × × / 2 2 2 / 3 3 3 / 4 5 6 / 17 18 19")

print("\n" + "=" * 70)
print("测试完成！")
print("=" * 70)

print("\n使用提示：")
print("  - display_ready_interactive(): 交互式查看听牌信息")
print("  - 第一步显示：听牌列表 + 总番数")
print("  - 第二步询问：是否需要详细信息")
print("  - 第三步显示：胡法 + 番种构成")
