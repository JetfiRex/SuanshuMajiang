"""
算术麻将番数计算 - 基于牌面信息的番种
包括：平胡、鸳鸯、全带彩、全彩、宝牌
"""

from typing import Optional
from collections import Counter
from hand_structure import Hand, Tile
from fan_calculator.fan_base import (
    FanType, FanResult, FanResults,
    get_tile_count, get_all_tiles_for_fan, TILE_COUNTS
)


def check_ping_hu(hand: Hand) -> Optional[FanResult]:
    """
    平胡 (4番)
    使用牌面张数至少4的牌的胡牌
    
    规则：
    - 不包括杠出来的牌
    - 只计手牌（不算鸣牌，除了吃碰）
    """
    # 获取不包括单张杠的牌
    tiles = get_all_tiles_for_fan(hand, include_single_gang=False)
    
    # 检查每张牌的牌面张数
    for tile in tiles:
        tile_count = get_tile_count(tile.value)
        if tile_count < 4:
            return None
    
    return FanResult(FanType.PING_HU)


def check_yang_yang(hand: Hand) -> Optional[FanResult]:
    """
    鸳鸯 (4番)
    出现某一对只有两张的牌的胡牌
    
    规则：
    - 不包括使用万用牌后代替的
    - 包括杠出来的
    - 每一对算一次
    """
    # 获取所有牌（包括单张杠）
    tiles = get_all_tiles_for_fan(hand, include_single_gang=True)
    
    # 统计每个牌值出现的次数
    value_counts = Counter()
    for tile in tiles:
        # 不计算万用牌代替的
        if not tile.is_joker_used:
            value_counts[tile.value] += 1
    
    # 计算有多少对只有2张的牌
    pair_count = 0
    for value, count in value_counts.items():
        tile_count = get_tile_count(value)
        # 只有2张的牌，且手中至少有2张
        if tile_count == 2 and count >= 2:
            # 每2张算一对
            pair_count += count // 2
    
    if pair_count > 0:
        return FanResult(FanType.YANG_YANG, count=pair_count, 
                        reason=f"{pair_count}对")
    
    return None


def check_quan_dai_cai(hand: Hand) -> Optional[FanResult]:
    """
    全带彩 (8番)
    由四个式子组成的胡牌，每一个式子都带有一张牌面张数等于2的牌
    
    规则：
    - 包括宝牌（dora），但不包括万用牌
    - 只检查手牌分组（算式和刻子）
    """
    # 必须有手牌分组
    if not hand.hand_groups:
        return None
    
    # 检查每一组是否都有张数=2的牌
    for group in hand.hand_groups:
        has_rare_tile = False
        for tile in group:
            # 不计算万用牌
            if tile.is_joker_used:
                continue
            
            tile_count = get_tile_count(tile.value)
            if tile_count == 2:
                has_rare_tile = True
                break
        
        # 如果有一组不满足，则不成立
        if not has_rare_tile:
            return None
    
    return FanResult(FanType.QUAN_DAI_CAI)


def check_quan_cai(hand: Hand) -> Optional[FanResult]:
    """
    全彩 (48番)
    只使用符号和整体张数小于等于2的牌（允许使用万用牌）
    
    规则：
    - 要么是符号牌
    - 要么是张数≤2的数字牌
    - 允许万用牌
    """
    # 获取所有牌（不包括单张杠）
    tiles = get_all_tiles_for_fan(hand, include_single_gang=False)
    
    from parser import SYMBOLS
    
    for tile in tiles:
        # 符号牌：允许
        if tile.value in SYMBOLS:
            continue
        
        # 万用牌：允许（因为规则中说"允许使用万用牌"）
        if tile.is_joker_used:
            continue
        
        # 数字牌：必须张数≤2
        tile_count = get_tile_count(tile.value)
        if tile_count > 2:
            return None
    
    return FanResult(FanType.QUAN_CAI)


def check_bao_pai(hand: Hand) -> Optional[FanResult]:
    """
    宝牌 (2番)
    胡牌时每张出现在牌组的宝牌以及单张杠出的万用牌
    
    规则：
    - 计算手牌中的dora牌数量
    - 单张杠出的万用牌也计算
    - 单张杠出的宝牌不能用作起胡番
    """
    # 获取所有牌（包括单张杠）
    tiles = get_all_tiles_for_fan(hand, include_single_gang=True)
    
    dora_count = 0
    joker_count = 0
    
    for tile in tiles:
        # 统计dora牌
        if tile.is_dora:
            dora_count += 1
    
    # 统计单张杠出的万用牌
    for melded_group in hand.melded_groups:
        if melded_group.group_type == 'single_gang':
            for tile in melded_group.tiles:
                # 万用牌（非数字、非符号）
                from parser import SYMBOLS, JOKERS
                if tile.value in JOKERS:
                    joker_count += 1
    
    total_count = dora_count + joker_count
    
    if total_count > 0:
        reason_parts = []
        if dora_count > 0:
            reason_parts.append(f"{dora_count}张dora")
        if joker_count > 0:
            reason_parts.append(f"{joker_count}张杠万用")
        
        return FanResult(
            FanType.BAO_PAI, 
            count=total_count,
            reason="+".join(reason_parts)
        )
    
    return None


def check_all_tile_info_fans(hand: Hand) -> FanResults:
    """
    检查所有基于牌面信息的番种
    
    参数：
        hand: Hand对象
    
    返回：
        FanResults对象
    """
    results = FanResults()
    
    # 48番
    fan = check_quan_cai(hand)
    if fan:
        results.add(fan)
    
    # 8番
    fan = check_quan_dai_cai(hand)
    if fan:
        results.add(fan)
    
    # 4番
    fan = check_ping_hu(hand)
    if fan:
        results.add(fan)
    
    fan = check_yang_yang(hand)
    if fan:
        results.add(fan)
    
    # 2番
    fan = check_bao_pai(hand)
    if fan:
        results.add(fan)
    
    return results
