"""
传统麻将和八小对胡牌判定器（支持万用牌）
用于算术麻将中的特殊胡法
"""

from collections import Counter
from itertools import combinations

class TraditionalMahjongChecker:
    """传统麻将胡牌判定器（支持万用牌）"""
    
    def __init__(self):
        # 数字到麻将牌面的映射
        self.num_to_tile = self._init_mapping()
        
        # 万用牌定义
        self.JOKER_TIAO = 'joker_tiao'  # 条子万用牌（代替1-9条）
        self.JOKER_TONG = 'joker_tong'  # 筒子万用牌（代替1-9筒）
        self.JOKER_WAN = 'joker_wan'    # 万子万用牌（代替1-9万）
        self.JOKER_SYMBOL = 'joker_symbol'  # 符号万用牌（代替中发白）
        
    def _init_mapping(self):
        """
        初始化数字到传统麻将牌面的映射
        """
        mapping = {}
        
        # 条子 (1-9)
        for i in range(1, 10):
            mapping[i] = ('条', i)
        
        # 筒子 (11-19)
        for i in range(1, 10):
            mapping[10 + i] = ('筒', i)
        
        # 万子 (按特定映射)
        wan_mapping = {
            21: 1, 32: 2, 35: 3, 24: 4, 25: 5,
            36: 6, 27: 7, 28: 8, 49: 9
        }
        for num, wan in wan_mapping.items():
            mapping[num] = ('万', wan)
        
        # 风牌
        mapping[10] = ('风', '北')
        mapping[20] = ('风', '南')
        mapping[30] = ('风', '东')
        mapping[40] = ('风', '西')
        
        # 箭牌（符号）
        mapping['+'] = ('箭', '中')
        mapping['×'] = ('箭', '发')
        mapping['∧'] = ('箭', '白')
        
        # 0 可以代替所有牌（在传统麻将中）
        mapping[0] = ('万用', 0)
        
        # 万用牌映射
        mapping['joker_tiao'] = ('万用', '条')
        mapping['joker_tong'] = ('万用', '筒')
        mapping['joker_wan'] = ('万用', '万')
        mapping['joker_symbol'] = ('万用', '箭')
        
        return mapping
    
    def convert_to_tiles(self, hand):
        """
        将算术麻将的数字牌转换为传统麻将牌面
        
        参数:
            hand: 算术麻将手牌列表
        
        返回:
            传统麻将牌面列表，格式: [('条', 1), ('筒', 5), ...]
            如果有牌无法转换，返回 None
        """
        tiles = []
        jokers = []  # 记录万用牌
        
        for card in hand:
            if card not in self.num_to_tile:
                return None, []
            
            tile = self.num_to_tile[card]
            
            # 分离万用牌和普通牌
            if tile[0] == '万用':
                jokers.append(tile)
            else:
                tiles.append(tile)
        
        return tiles, jokers
    
    def can_win_traditional(self, hand):
        """
        判断是否能按传统麻将规则胡牌（4组面子+2对将）
        支持万用牌
        
        参数:
            hand: 算术麻将手牌列表（应该是16张）
        
        返回:
            (是否能胡, 胡牌组合)
        """
        tiles, jokers = self.convert_to_tiles(hand)
        if tiles is None:
            return False, []
        
        if len(tiles) + len(jokers) != 16:
            return False, []
        
        # 尝试所有万用牌的分配方案
        return self._try_win_with_jokers(tiles, jokers)
    
    def _try_win_with_jokers(self, tiles, jokers):
        """
        尝试使用万用牌组成胡牌
        """
        if len(jokers) == 0:
            # 没有万用牌，直接检查
            return self._check_win_no_joker(tiles)
        
        # 生成所有可能的万用牌替换方案
        all_possible_tiles = self._get_all_possible_tiles()
        
        # 递归尝试所有万用牌的分配
        return self._try_joker_assignments(tiles, jokers, all_possible_tiles, 0, [])
    
    def _try_joker_assignments(self, tiles, jokers, all_tiles, joker_idx, assignments):
        """
        递归尝试所有万用牌的替换方案
        """
        if joker_idx >= len(jokers):
            # 所有万用牌都已分配，检查是否能胡
            test_tiles = tiles + assignments
            return self._check_win_no_joker(test_tiles)
        
        joker = jokers[joker_idx]
        joker_type = joker[1]
        
        # 根据万用牌类型确定可替换的牌
        if joker_type == '条':
            possible = [('条', i) for i in range(1, 10)]
        elif joker_type == '筒':
            possible = [('筒', i) for i in range(1, 10)]
        elif joker_type == '万':
            possible = [('万', i) for i in range(1, 10)]
        elif joker_type == '箭':
            possible = [('箭', '中'), ('箭', '发'), ('箭', '白')]
        elif joker_type == 0:  # 数字0，可以代替所有牌
            possible = all_tiles
        else:
            return False, []
        
        # 尝试每种可能的替换
        for tile in possible:
            new_assignments = assignments + [tile]
            success, result = self._try_joker_assignments(
                tiles, jokers, all_tiles, joker_idx + 1, new_assignments
            )
            if success:
                return True, result
        
        return False, []
    
    def _get_all_possible_tiles(self):
        """获取所有可能的麻将牌面"""
        tiles = []
        # 条筒万 1-9
        for suit in ['条', '筒', '万']:
            for i in range(1, 10):
                tiles.append((suit, i))
        # 风牌
        for wind in ['北', '南', '东', '西']:
            tiles.append(('风', wind))
        # 箭牌
        for arrow in ['中', '发', '白']:
            tiles.append(('箭', arrow))
        return tiles
    
    def _check_win_no_joker(self, tiles):
        """
        检查无万用牌的情况下能否胡牌（4组面子+2对将）
        """
        if len(tiles) != 16:
            return False, []
        
        tile_counter = Counter(tiles)
        tiles_with_pairs = [tile for tile, count in tile_counter.items() if count >= 2]
        
        # 尝试所有可能的两对将的组合
        for i, tile1 in enumerate(tiles_with_pairs):
            for j, tile2 in enumerate(tiles_with_pairs):
                if i > j:
                    continue
                
                # tile1 和 tile2 可以相同或不同
                if tile1 == tile2 and tile_counter[tile1] < 4:
                    continue
                
                # 尝试移除这两对将
                remaining = tiles.copy()
                try:
                    remaining.remove(tile1)
                    remaining.remove(tile1)
                    remaining.remove(tile2)
                    remaining.remove(tile2)
                except ValueError:
                    continue
                
                # 检查剩余12张能否组成4组面子
                melds = []
                if self._can_form_melds_with_record(remaining, melds):
                    result = [('将', tile1, tile1), ('将', tile2, tile2)] + melds
                    return True, result

        return False, []

    def _can_form_melds(self, tiles):
        """判断给定的牌能否组成面子（刻子或顺子）"""
        if len(tiles) == 0:
            return True

        if len(tiles) % 3 != 0:
            return False

        tile_counter = Counter(tiles)
        return self._try_remove_melds(tile_counter)

    def _try_remove_melds(self, counter):
        """递归尝试移除面子"""
        if sum(counter.values()) == 0:
            return True

        # 找到第一张牌
        first_tile = None
        for tile, count in counter.items():
            if count > 0:
                first_tile = tile
                break

        if first_tile is None:
            return True

        suit, value = first_tile

        # 尝试1: 刻子（三张相同）
        if counter[first_tile] >= 3:
            counter[first_tile] -= 3
            if self._try_remove_melds(counter):
                return True
            counter[first_tile] += 3

        # 尝试2: 顺子（只对数字牌，且同花色）
        if isinstance(value, int) and value <= 7:
            tile2 = (suit, value + 1)
            tile3 = (suit, value + 2)

            if counter[tile2] > 0 and counter[tile3] > 0:
                counter[first_tile] -= 1
                counter[tile2] -= 1
                counter[tile3] -= 1

                if self._try_remove_melds(counter):
                    return True

                counter[first_tile] += 1
                counter[tile2] += 1
                counter[tile3] += 1

        return False

    def _can_form_melds_with_record(self, tiles, melds):
        """判断给定的牌能否组成面子（刻子或顺子），并记录面子组合"""
        if len(tiles) == 0:
            return True

        if len(tiles) % 3 != 0:
            return False

        tile_counter = Counter(tiles)
        return self._try_remove_melds_with_record(tile_counter, melds)

    def _try_remove_melds_with_record(self, counter, melds):
        """递归尝试移除面子，并记录"""
        if sum(counter.values()) == 0:
            return True

        # 找到第一张牌
        first_tile = None
        for tile, count in counter.items():
            if count > 0:
                first_tile = tile
                break

        if first_tile is None:
            return True

        suit, value = first_tile

        # 尝试1: 刻子（三张相同）
        if counter[first_tile] >= 3:
            counter[first_tile] -= 3
            melds.append(('刻子', first_tile, first_tile, first_tile))
            if self._try_remove_melds_with_record(counter, melds):
                return True
            melds.pop()
            counter[first_tile] += 3

        # 尝试2: 顺子（只对数字牌，且同花色）
        if isinstance(value, int) and value <= 7:
            tile2 = (suit, value + 1)
            tile3 = (suit, value + 2)

            if counter[tile2] > 0 and counter[tile3] > 0:
                counter[first_tile] -= 1
                counter[tile2] -= 1
                counter[tile3] -= 1
                melds.append(('顺子', first_tile, tile2, tile3))

                if self._try_remove_melds_with_record(counter, melds):
                    return True

                melds.pop()
                counter[first_tile] += 1
                counter[tile2] += 1
                counter[tile3] += 1
        
        return False
    
    def is_ready_traditional(self, hand):
        """
        判断15张牌是否听牌（传统麻将）
        支持万用牌
        
        参数:
            hand: 15张牌的列表
        
        返回:
            (是否听牌, 听的牌列表)
        """
        if len(hand) != 15:
            return False, []
        
        # 所有可能的牌（算术麻将的数字表示）
        all_possible_nums = self._get_all_possible_nums()
        
        ready_tiles = []
        
        for num in all_possible_nums:
            test_hand = hand + [num]
            can_win, _ = self.can_win_traditional(test_hand)
            if can_win:
                ready_tiles.append(num)
        
        return len(ready_tiles) > 0, ready_tiles
    
    def _get_all_possible_nums(self):
        """获取所有可能的牌（算术麻将数字表示）"""
        nums = []
        # 条子 1-9
        for i in range(1, 10):
            nums.append(i)
        # 筒子 11-19
        for i in range(11, 20):
            nums.append(i)
        # 万子
        for num in [21, 32, 35, 24, 25, 36, 27, 28, 49]:
            nums.append(num)
        # 风牌
        for wind in [10, 20, 30, 40]:
            nums.append(wind)
        # 符号
        for symbol in ['+', '×', '∧']:
            nums.append(symbol)
        return nums
    
    def _tile_to_num(self, tile_face):
        """将麻将牌面转换回数字"""
        for num, face in self.num_to_tile.items():
            if face == tile_face:
                return num
        return None


class EightPairsChecker:
    """八小对胡牌判定器（支持万用牌，但0不是万用牌）"""
    
    def __init__(self):
        self.JOKER_TIAO = 'joker_tiao'
        self.JOKER_TONG = 'joker_tong'
        self.JOKER_WAN = 'joker_wan'
        self.JOKER_SYMBOL = 'joker_symbol'
    
    def can_win_eight_pairs(self, hand):
        """
        判断是否能胡八小对（8个对子，门清）
        支持万用牌，但0在八小对中不是万用牌，就是普通的0
        
        参数:
            hand: 16张牌的列表
        
        返回:
            (是否能胡, 对子列表)
        """
        if len(hand) != 16:
            return False, []
        
        # 分离普通牌和万用牌
        # 注意：0在八小对中是普通牌，不是万用牌
        normal_tiles = []
        jokers = []
        
        for tile in hand:
            if tile in [self.JOKER_TIAO, self.JOKER_TONG, 
                       self.JOKER_WAN, self.JOKER_SYMBOL]:
                jokers.append(tile)
            else:
                # 0也算普通牌
                normal_tiles.append(tile)
        
        # 尝试用万用牌组成对子
        return self._try_eight_pairs_with_jokers(normal_tiles, jokers)
    
    def _try_eight_pairs_with_jokers(self, tiles, jokers):
        """尝试用万用牌组成八小对"""
        counter = Counter(tiles)
        
        # 统计已有的对子
        pairs = []
        singles = []
        
        for tile, count in counter.items():
            pairs_count = count // 2
            for _ in range(pairs_count):
                pairs.append((tile, tile))
            if count % 2 == 1:
                singles.append(tile)
        
        # 需要的对子数
        needed_pairs = 8 - len(pairs)
        
        # 检查万用牌是否足够
        # 每个单张需要1个万用牌配对，剩余的万用牌需要2个凑成一对
        if len(singles) > len(jokers):
            return False, []
        
        jokers_after_pairing_singles = len(jokers) - len(singles)
        if jokers_after_pairing_singles % 2 != 0:
            return False, []
        
        pairs_from_jokers = len(singles) + jokers_after_pairing_singles // 2
        
        if len(pairs) + pairs_from_jokers == 8:
            # 可以组成八小对
            for single in singles:
                pairs.append((single, 'joker'))
            for _ in range(jokers_after_pairing_singles // 2):
                pairs.append(('joker', 'joker'))
            return True, pairs
        
        return False, []
    
    def is_ready_eight_pairs(self, hand):
        """
        判断15张牌是否听八小对
        支持万用牌，但0在八小对中是普通牌
        
        参数:
            hand: 15张牌的列表
        
        返回:
            (是否听牌, 听的牌列表)
        """
        if len(hand) != 15:
            return False, []
        
        # 分离普通牌和万用牌
        # 0在八小对中是普通牌
        normal_tiles = []
        jokers = []
        
        for tile in hand:
            if tile in [self.JOKER_TIAO, self.JOKER_TONG, 
                       self.JOKER_WAN, self.JOKER_SYMBOL]:
                jokers.append(tile)
            else:
                normal_tiles.append(tile)
        
        counter = Counter(normal_tiles)
        
        # 统计对子和单张
        pairs_count = sum(count // 2 for count in counter.values())
        singles = [tile for tile, count in counter.items() if count % 2 == 1]
        
        # 情况1: 已有7个完整对子，单张配万用牌
        if pairs_count == 7 and len(singles) == 1:
            # 听这张单牌
            return True, singles
        
        # 情况2: 考虑万用牌的组合
        # 使用万用牌后的对子数
        jokers_for_singles = min(len(singles), len(jokers))
        remaining_jokers = len(jokers) - jokers_for_singles
        
        total_pairs = pairs_count + jokers_for_singles + remaining_jokers // 2
        remaining_singles = len(singles) - jokers_for_singles + remaining_jokers % 2
        
        if total_pairs == 7 and remaining_singles == 1:
            # 找出哪张是单张
            if len(singles) > len(jokers):
                # 有单张没被配对
                return True, [s for s in singles if counter[s] % 2 == 1]
            elif remaining_jokers % 2 == 1:
                # 万用牌有剩余单张，任意牌都可以
                # 返回所有可能的牌
                all_tiles = set(range(50)) | {'+', '×', '∧'}
                return True, sorted(list(all_tiles), key=lambda x: (x not in {'+', '×', '∧'}, x))
        
        return False, []


# 测试函数
def test_traditional_and_eight_pairs():
    """测试传统麻将和八小对（含万用牌）"""
    
    print("=" * 60)
    print("传统麻将和八小对判定器测试（支持万用牌）")
    print("=" * 60)
    
    trad_checker = TraditionalMahjongChecker()
    eight_checker = EightPairsChecker()
    
    # 测试1: 传统麻将胡牌（无万用牌）
    print("\n【测试1】传统麻将胡牌（无万用牌）")
    hand1 = [1, 2, 3, 4, 5, 6, 7, 7, 7, 8, 8, 8, 11, 11, 12, 12]
    print(f"手牌: {hand1}")
    can_win, result = trad_checker.can_win_traditional(hand1)
    print(f"能否胡牌: {can_win}")
    
    # 测试2: 传统麻将胡牌（有万用牌）
    print("\n【测试2】传统麻将胡牌（有万用牌）")
    hand2 = [1, 2, 3, 4, 5, 6, 7, 7, 7, 8, 8, 8, 11, 11, 12, 'joker_tong']
    print(f"手牌: {hand2}")
    can_win, result = trad_checker.can_win_traditional(hand2)
    print(f"能否胡牌: {can_win}")
    
    # 测试3: 八小对（无万用牌）
    print("\n【测试3】八小对（无万用牌）")
    hand3 = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
    print(f"手牌: {hand3}")
    can_win, pairs = eight_checker.can_win_eight_pairs(hand3)
    print(f"能否胡八小对: {can_win}")
    
    # 测试4: 八小对（有万用牌）
    print("\n【测试4】八小对（有万用牌）")
    hand4 = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 0, 0]
    print(f"手牌: {hand4}")
    can_win, pairs = eight_checker.can_win_eight_pairs(hand4)
    print(f"能否胡八小对: {can_win}")


if __name__ == "__main__":
    test_traditional_and_eight_pairs()