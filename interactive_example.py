#!/usr/bin/env python3
"""
算术麻将系统 v1.7 - 模式3/4交互式使用示例

使用方法：
1. 运行脚本
2. 查看听牌列表和每张牌的总番数
3. 选择是否查看详细信息（y/n）
4. 如果选择y，查看每张听牌的胡法和番种构成
"""

import sys
sys.path.insert(0, '/home/claude/arithmetic_mahjong_v1.6_FINAL')

from mahjong_checker import ArithmeticMahjong

def main():
    print("=" * 70)
    print("算术麻将系统 v1.7 - 模式3/4交互式听牌查询")
    print("=" * 70)
    
    mjong = ArithmeticMahjong(require_sum_gte_10=True, min_fan=8)
    
    # 示例1：15张听牌
    print("\n【示例1：15张听牌 - 算术麻将和传统麻将】")
    print("-" * 70)
    hand_15 = [1, '+', 15, 16, 2, '+', 13, 15, 3, '+', 14, 17, '×', '×', '×']
    print(f"手牌（15张）: {' '.join(map(str, hand_15))}")
    print()
    
    # 调用交互式显示
    mjong.display_ready_interactive(hand_15)
    
    # 示例2：11张听牌（部分组合）
    print("\n\n" + "=" * 70)
    print("\n【示例2：11张听牌 - 算术麻将（部分组合）】")
    print("-" * 70)
    hand_11 = [1, '+', 15, 16, 2, '+', 13, 15, 3, '+', 14]
    print(f"手牌（11张）: {' '.join(map(str, hand_11))}")
    print()
    
    mjong.display_ready_interactive(hand_11)
    
    print("\n\n" + "=" * 70)
    print("示例完成！")
    print("=" * 70)

if __name__ == '__main__':
    main()
