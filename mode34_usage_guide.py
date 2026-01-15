#!/usr/bin/env python3
"""
算术麻将系统 v1.7 - 模式3和4的详细信息功能使用指南

新增功能：
1. is_ready() 方法新增 return_details 参数
2. 当 return_details=True 时，返回每张听牌的：
   - 胡牌组合（分组方案）
   - 番数信息
   - 是否满足起胡条件
"""

import sys
sys.path.insert(0, '/home/claude/arithmetic_mahjong_v1.6_FINAL')

from mahjong_checker import ArithmeticMahjong

print("=" * 70)
print("算术麻将系统 v1.7 - 模式3/4使用示例")
print("=" * 70)

# 初始化
mjong = ArithmeticMahjong(require_sum_gte_10=True, min_fan=8)

# ============================================================
# 示例1：简单模式 - 只返回听牌列表（向后兼容）
# ============================================================
print("\n【示例1：简单模式 - 只返回听牌列表】")
print("-" * 70)
hand_15 = [1, '+', 15, 16, 2, '+', 13, 15, 3, '+', 14, 17, '×', '×', '×']

is_ready, ready_info = mjong.is_ready(hand_15)  # 默认 return_details=False

print(f"手牌: {' '.join(map(str, hand_15))}")
print(f"是否听牌: {is_ready}")
if is_ready:
    for win_type, tiles in ready_info.items():
        print(f"  {win_type}: {tiles}")

# ============================================================
# 示例2：详细模式 - 返回分组和番数信息
# ============================================================
print("\n" + "=" * 70)
print("\n【示例2：详细模式 - 获取每张听牌的番数】")
print("-" * 70)

is_ready, ready_info = mjong.is_ready(hand_15, return_details=True)

if is_ready:
    # 遍历每种胡法类型
    for win_type, info in ready_info.items():
        print(f"\n{win_type}:")
        print(f"  共听 {len(info['tiles'])} 张牌")
        
        # 遍历每张听牌
        for tile in info['tiles']:
            detail = info['details'][tile]
            
            # 基本信息
            print(f"\n  → 听 {tile}:")
            print(f"     胡牌类型: {detail['win_type']}")
            
            # 番数信息
            if detail['fan_info']:
                fan_info = detail['fan_info']
                print(f"     总番数: {fan_info['total_fan']}番")
                print(f"     满足起胡: {'✅ 是' if fan_info['can_start'] else '❌ 否'}")
                
                # 番种明细
                print(f"     番种明细:")
                for fan_result in fan_info['fan_result'].results:
                    print(f"       • {fan_result}")
            else:
                print(f"     番数: N/A（部分组合）")

# ============================================================
# 示例3：分析最优听牌
# ============================================================
print("\n" + "=" * 70)
print("\n【示例3：分析最优听牌（番数最高的）】")
print("-" * 70)

is_ready, ready_info = mjong.is_ready(hand_15, return_details=True)

if is_ready:
    max_fan = 0
    best_tile = None
    best_win_type = None
    
    # 遍历所有胡法和听牌
    for win_type, info in ready_info.items():
        for tile, detail in info['details'].items():
            if detail['fan_info'] and detail['fan_info']['total_fan'] > max_fan:
                max_fan = detail['fan_info']['total_fan']
                best_tile = tile
                best_win_type = win_type
    
    print(f"最优听牌: 听 {best_tile} ({best_win_type})")
    print(f"番数: {max_fan}番")

# ============================================================
# 示例4：过滤满足起胡条件的听牌
# ============================================================
print("\n" + "=" * 70)
print("\n【示例4：只显示满足起胡的听牌】")
print("-" * 70)

is_ready, ready_info = mjong.is_ready(hand_15, return_details=True)

if is_ready:
    print("满足起胡条件（≥8番）的听牌：")
    
    for win_type, info in ready_info.items():
        valid_tiles = []
        
        for tile, detail in info['details'].items():
            if detail['fan_info'] and detail['fan_info']['can_start']:
                valid_tiles.append((tile, detail['fan_info']['total_fan']))
        
        if valid_tiles:
            # 按番数排序
            valid_tiles.sort(key=lambda x: x[1], reverse=True)
            
            print(f"\n  {win_type}:")
            for tile, fan in valid_tiles:
                print(f"    • 听 {tile}: {fan}番")

# ============================================================
# 示例5：模式4 - 11张/7张/3张听牌
# ============================================================
print("\n" + "=" * 70)
print("\n【示例5：模式4 - 部分组合听牌】")
print("-" * 70)

hand_11 = [1, '+', 15, 16, 2, '+', 13, 15, 3, '+', 14]
print(f"手牌（11张）: {' '.join(map(str, hand_11))}")

is_ready, ready_info = mjong.is_ready(hand_11, return_details=True)

if is_ready:
    for win_type, info in ready_info.items():
        print(f"\n  {win_type}: 听 {len(info['tiles'])} 张牌")
        
        # 显示前5张
        for tile in info['tiles'][:5]:
            detail = info['details'][tile]
            print(f"    • {tile}: {len(detail['groups'])}组")
        
        if len(info['tiles']) > 5:
            print(f"    ... 还有 {len(info['tiles']) - 5} 张")

print("\n" + "=" * 70)
print("使用指南完成！")
print("=" * 70)

print("\n" + "=" * 70)
print("API 总结")
print("=" * 70)
print("""
is_ready(hand, return_details=False)

参数：
  - hand: 牌列表（15/11/7/3张）
  - return_details: 是否返回详细信息（默认False）

返回：
  (is_ready: bool, ready_info: dict)

return_details=False 时：
  ready_info = {
      '算术麻将': [听牌列表],
      '传统麻将': [听牌列表],
      '八小对': [听牌列表]
  }

return_details=True 时：
  ready_info = {
      '算术麻将': {
          'tiles': [听牌列表],
          'details': {
              tile: {
                  'groups': [分组],
                  'win_type': '胡牌类型',
                  'fan_info': {
                      'total_fan': 总番数,
                      'can_start': 是否满足起胡,
                      'fan_result': FanResults对象
                  } or None
              }
          }
      }
  }
""")
