"""
特殊胜利判定器
处理5种特殊胡法：八仙过海、四仙过海、天龙、地龙、十三幺
这些胡法不需要分组，只看牌的集合
"""

from typing import List, Tuple, Set
from calculator_base.constants import PLUS, MULTIPLY, POWER

# 宝牌定义
DORA_TILES = ['11d', '13d', '17d', '19d']

# 十三幺必须的牌
SHI_SAN_YAO_TILES = [1, 9, 10, 11, 19, 20, 21, 49, 30, 40, PLUS, MULTIPLY, POWER]


class SpecialWinningChecker:
    """特殊胜利判定器"""
    
    def __init__(self):
        pass
    
    def _extract_all_tiles(self, hand):
        """
        提取所有牌（包括手牌、鸣牌、单张杠）
        
        返回：
        - all_tiles: 所有牌的列表
        - single_gang_count: 单张杠数量
        """
        all_tiles = []
        single_gang_count = 0
        
        # 如果是Hand对象
        if hasattr(hand, 'hand_groups'):
            # 手牌分组
            for group in hand.hand_groups:
                for tile in group:
                    # 提取tile的value
                    if hasattr(tile, 'value'):
                        all_tiles.append(tile.value)
                    else:
                        all_tiles.append(tile)
            
            # 鸣牌
            if hasattr(hand, 'melded_groups'):
                for melded in hand.melded_groups:
                    if melded.group_type == 'single_gang':
                        single_gang_count += 1
                        # 单张杠的牌也要算进去
                        for tile in melded.tiles:
                            if hasattr(tile, 'value'):
                                all_tiles.append(tile.value)
                            else:
                                all_tiles.append(tile)
                    else:
                        # 其他鸣牌（吃、碰、明杠、暗杠）
                        for tile in melded.tiles:
                            if hasattr(tile, 'value'):
                                all_tiles.append(tile.value)
                            else:
                                all_tiles.append(tile)
        else:
            # 如果是列表
            all_tiles = hand
        
        return all_tiles, single_gang_count
    
    def _count_single_gangs(self, hand):
        """统计单张杠数量（宝牌和万用牌）"""
        if not hasattr(hand, 'melded_groups'):
            return 0, 0
        
        dora_count = 0
        joker_count = 0
        
        # 万用牌类型
        joker_types = ['joker_tiao', 'joker_tong', 'joker_wan', 'joker_symbol']
        
        for melded in hand.melded_groups:
            if melded.group_type == 'single_gang':
                tile = melded.tiles[0]
                tile_str = str(tile)
                
                # 检查是否是宝牌
                if tile_str in DORA_TILES or (hasattr(tile, 'is_dora') and tile.is_dora):
                    dora_count += 1
                # 检查是否是万用牌
                elif tile_str in joker_types:
                    joker_count += 1
                elif hasattr(tile, 'is_joker_used') and tile.is_joker_used:
                    joker_count += 1
        
        return dora_count, joker_count
    
    def can_win_ba_xian_guo_hai(self, hand) -> Tuple[bool, None]:
        """
        判断是否能胡八仙过海（88番）
        规则：8种单张杠（4宝牌 + 4万用牌）
        """
        dora_count, joker_count = self._count_single_gangs(hand)
        
        # 必须有4个宝牌单张杠 + 4个万用牌单张杠
        if dora_count == 4 and joker_count == 4:
            return True, None
        
        return False, None
    
    def can_win_si_xian_guo_hai(self, hand) -> Tuple[bool, None]:
        """
        判断是否能胡四仙过海（24番）
        规则：4个宝牌或4个万用牌单张杠
        """
        dora_count, joker_count = self._count_single_gangs(hand)
        
        # 4个宝牌单张杠 或 4个万用牌单张杠
        if dora_count >= 4 or joker_count >= 4:
            return True, None
        
        return False, None
    
    def can_win_tian_long(self, hand) -> Tuple[bool, None]:
        """
        判断是否能胡天龙（88番）
        规则：手牌+鸣牌+单张杠中有16个连续的数字（去重后）
        """
        all_tiles, _ = self._extract_all_tiles(hand)
        
        # 只提取数字牌
        numbers = []
        for tile in all_tiles:
            if isinstance(tile, int) and 0 <= tile <= 49:
                numbers.append(tile)
        
        # 去重并排序
        unique_numbers = sorted(set(numbers))
        
        # 检查是否有16个连续数字
        if len(unique_numbers) < 16:
            return False, None
        
        for i in range(len(unique_numbers) - 15):
            is_continuous = True
            for j in range(15):
                if unique_numbers[i + j + 1] != unique_numbers[i + j] + 1:
                    is_continuous = False
                    break
            if is_continuous:
                return True, None
        
        return False, None
    
    def can_win_di_long(self, hand) -> Tuple[bool, None]:
        """
        判断是否能胡地龙（32番）
        规则：手牌+鸣牌+单张杠中有12项连续的等差数列
        公差：1-4，首项<50
        """
        all_tiles, _ = self._extract_all_tiles(hand)
        
        # 只提取数字牌
        numbers = []
        for tile in all_tiles:
            if isinstance(tile, int) and 0 <= tile <= 49:
                numbers.append(tile)
        
        # 去重
        unique_numbers = set(numbers)
        
        # 尝试所有可能的首项和公差
        for start in range(50):  # 首项<50
            for diff in range(1, 5):  # 公差1-4
                # 检查是否存在12项等差数列
                sequence = [start + i * diff for i in range(12)]
                if all(num in unique_numbers for num in sequence):
                    return True, None
        
        return False, None
    
    def can_win_shi_san_yao(self, hand) -> Tuple[bool, None]:
        """
        判断是否能胡十三幺（88番）
        规则：必须有 1,9,10,11,19,20,21,49,30,40,+,×,^ 各至少1张
        """
        all_tiles, _ = self._extract_all_tiles(hand)
        
        # 统计每种牌的数量
        tile_count = {}
        for tile in all_tiles:
            tile_count[tile] = tile_count.get(tile, 0) + 1
        
        # 检查13种牌是否都至少有1张
        for required_tile in SHI_SAN_YAO_TILES:
            if tile_count.get(required_tile, 0) < 1:
                return False, None
        
        return True, None
    
    def is_ready_tian_long(self, hand) -> Tuple[bool, List]:
        """
        判断是否听天龙
        返回：(是否听牌, 听的牌列表)
        """
        all_tiles, _ = self._extract_all_tiles(hand)
        
        # 只提取数字牌
        numbers = []
        for tile in all_tiles:
            if isinstance(tile, int) and 0 <= tile <= 49:
                numbers.append(tile)
        
        # 去重
        unique_numbers = sorted(set(numbers))
        
        # 如果已经有16个连续数字，听所有牌
        for i in range(len(unique_numbers) - 15):
            is_continuous = True
            for j in range(15):
                if unique_numbers[i + j + 1] != unique_numbers[i + j] + 1:
                    is_continuous = False
                    break
            if is_continuous:
                # 已满足天龙，听所有牌
                from calculator_base.constants import ALL_TILES
                return True, ALL_TILES.copy()
        
        # 否则，找出加上哪张牌能组成16个连续数字
        ready_tiles = []
        
        # 尝试所有可能的牌
        for test_tile in range(50):
            test_numbers = unique_numbers + [test_tile]
            test_unique = sorted(set(test_numbers))
            
            # 检查是否有16个连续数字
            if len(test_unique) >= 16:
                for i in range(len(test_unique) - 15):
                    is_continuous = True
                    for j in range(15):
                        if test_unique[i + j + 1] != test_unique[i + j] + 1:
                            is_continuous = False
                            break
                    if is_continuous:
                        ready_tiles.append(test_tile)
                        break
        
        return len(ready_tiles) > 0, ready_tiles
    
    def is_ready_di_long(self, hand) -> Tuple[bool, List]:
        """
        判断是否听地龙
        返回：(是否听牌, 听的牌列表)
        """
        all_tiles, _ = self._extract_all_tiles(hand)
        
        # 只提取数字牌
        numbers = []
        for tile in all_tiles:
            if isinstance(tile, int) and 0 <= tile <= 49:
                numbers.append(tile)
        
        # 去重
        unique_numbers = set(numbers)
        
        # 如果已经有12项等差数列，听所有牌
        for start in range(50):
            for diff in range(1, 5):
                sequence = [start + i * diff for i in range(12)]
                if all(num in unique_numbers for num in sequence):
                    # 已满足地龙，听所有牌
                    from calculator_base.constants import ALL_TILES
                    return True, ALL_TILES.copy()
        
        # 否则，找出加上哪张牌能组成12项等差数列
        ready_tiles = []
        
        for test_tile in range(50):
            test_numbers = unique_numbers | {test_tile}
            
            for start in range(50):
                for diff in range(1, 5):
                    sequence = [start + i * diff for i in range(12)]
                    if all(num in test_numbers for num in sequence):
                        ready_tiles.append(test_tile)
                        break
                if test_tile in ready_tiles:
                    break
        
        return len(ready_tiles) > 0, list(set(ready_tiles))
    
    def is_ready_shi_san_yao(self, hand) -> Tuple[bool, List]:
        """
        判断是否听十三幺
        返回：(是否听牌, 听的牌列表)
        """
        all_tiles, _ = self._extract_all_tiles(hand)
        
        # 统计每种牌的数量
        tile_count = {}
        for tile in all_tiles:
            tile_count[tile] = tile_count.get(tile, 0) + 1
        
        # 如果已经满足十三幺，听所有牌
        all_satisfied = all(tile_count.get(tile, 0) >= 1 for tile in SHI_SAN_YAO_TILES)
        if all_satisfied:
            from calculator_base.constants import ALL_TILES
            return True, ALL_TILES.copy()
        
        # 否则，找出还缺哪些牌
        ready_tiles = []
        for required_tile in SHI_SAN_YAO_TILES:
            if tile_count.get(required_tile, 0) < 1:
                ready_tiles.append(required_tile)
        
        if ready_tiles == 1:
            return True, ready_tiles
        else: return False, ready_tiles
