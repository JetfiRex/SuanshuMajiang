from itertools import combinations, product
from collections import Counter

from parser import (
    PLUS, MULTIPLY, POWER, SYMBOLS,
    JOKER_TIAO, JOKER_TONG, JOKER_WAN, JOKER_SYMBOL, JOKERS,
    ALL_TILES,
    parse_hand, format_hand,
)

# 导入传统麻将和八小对判定器
# 注意：需要将 traditional_mahjong.py 放在同一目录下
try:
    from traditional_mahjong import TraditionalMahjongChecker, EightPairsChecker

    TRADITIONAL_AVAILABLE = True
except ImportError:
    TRADITIONAL_AVAILABLE = False
    print("警告: 未找到 traditional_mahjong.py，传统麻将和八小对功能将不可用")


class ArithmeticMahjong:
    """算术麻将胡牌判定器（支持万用牌）"""

    def __init__(self, require_sum_gte_10=True):
        """
        初始化算术麻将判定器

        参数:
            require_sum_gte_10: bool, 是否要求加法算式的和必须>=10
                               True: 标准规则，加法和必须>=10（默认）
                               False: 新手规则，加法和可以<10
        """
        # 使用 parser 模块的常量
        self.symbols = SYMBOLS

        # 规则设置
        self.require_sum_gte_10 = require_sum_gte_10

        # 所有可能的牌（从 parser 模块导入）
        self.all_tiles = ALL_TILES.copy()

        # 牌库中存在的牌（用于判断是否需要标注"需要万用"）
        self.tiles_in_pool = ALL_TILES.copy()

        # 初始化传统麻将和八小对判定器
        if TRADITIONAL_AVAILABLE:
            self.traditional_checker = TraditionalMahjongChecker()
            self.eight_pairs_checker = EightPairsChecker()
        else:
            self.traditional_checker = None
            self.eight_pairs_checker = None

    def is_valid_formula(self, tiles):
        """
        判断4张牌是否构成有效算式（支持万用牌）
        算式形式: a op b = c
        tiles: 包含4张牌的列表
        """
        if len(tiles) != 4:
            return False

        # 分离万用牌和普通牌
        jokers = [t for t in tiles if t in JOKERS]
        normal = [t for t in tiles if t not in jokers]

        # 如果有万用牌，需要尝试所有可能的替换
        if len(jokers) > 0:
            return self._check_formula_with_jokers(normal, jokers)

        # 没有万用牌，按原逻辑处理
        nums = []
        op = None

        for t in tiles:
            if t in SYMBOLS:
                if op is not None:
                    return False
                op = t
            else:
                nums.append(t)

        if len(nums) != 3 or op is None:
            return False

        # 尝试所有可能的组合
        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                k = 3 - i - j
                a, b, c = nums[i], nums[j], nums[k]

                try:
                    if op == PLUS:
                        if a + b == c:
                            if self.require_sum_gte_10 and c < 10:
                                continue
                            return True
                    elif op == MULTIPLY:
                        if a * b == c:
                            return True
                    elif op == POWER:
                        if a > 100 or b > 10:
                            continue
                        if a ** b == c:
                            return True
                except (OverflowError, ValueError):
                    continue

        return False

    def _check_formula_with_jokers(self, normal, jokers):
        """检查带万用牌的算式是否合法"""
        # 为每个万用牌生成可能的替换值
        possible_values = []
        for joker in jokers:
            if joker == JOKER_TIAO:
                possible_values.append(list(range(10)))
            elif joker == JOKER_TONG:
                possible_values.append(list(range(10, 20)))
            elif joker == JOKER_WAN:
                possible_values.append(list(range(20, 50)))
            elif joker == JOKER_SYMBOL:
                possible_values.append([PLUS, MULTIPLY, POWER])

        # 生成所有可能的组合
        for combo in product(*possible_values):
            test_tiles = normal + list(combo)
            if self._check_single_formula(test_tiles):
                return True

        return False

    def _check_single_formula(self, tiles):
        """检查单个算式（不含万用牌）"""
        nums = []
        op = None

        for t in tiles:
            if t in SYMBOLS:
                if op is not None:
                    return False
                op = t
            else:
                nums.append(t)

        if len(nums) != 3 or op is None:
            return False

        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                k = 3 - i - j
                a, b, c = nums[i], nums[j], nums[k]

                try:
                    if op == PLUS:
                        if a + b == c:
                            if self.require_sum_gte_10 and c < 10:
                                continue
                            return True
                    elif op == MULTIPLY:
                        if a * b == c:
                            return True
                    elif op == POWER:
                        if a > 100 or b > 10:
                            continue
                        if a ** b == c:
                            return True
                except (OverflowError, ValueError):
                    continue

        return False

    def is_kezi(self, tiles):
        """判断4张牌是否构成刻子（4张相同）"""
        return len(tiles) == 4 and len(set(tiles)) == 1

    def is_valid_group(self, tiles):
        """判断4张牌是否构成有效组（算式或刻子）"""
        # 先检查刻子（更快）
        if self.is_kezi(tiles):
            return True
        return self.is_valid_formula(tiles)

    def can_win(self, hand):
        """
        判断给定的16张牌是否能胡牌
        会检查：
        1. 标准算术麻将胡法（4组算式/刻子）
        2. 传统麻将胡法（4组面子+2对将）
        3. 八小对胡法（8个对子）

        hand: 牌的列表，例如 [1, 2, 3, '+', 5, 5, 5, 5, ...]
        返回: (是否能胡, 分组方案, 胡牌类型)
        """
        if len(hand) != 16:
            return False, [], None

        # 1. 检查标准算术麻将胡法
        can_win_arith, groups = self._partition_optimized(hand)
        if can_win_arith:
            return True, groups, "算术麻将"

        # 2. 检查传统麻将胡法
        if self.traditional_checker is not None:
            can_win_trad, result = self.traditional_checker.can_win_traditional(hand)
            if can_win_trad:
                return True, result, "传统麻将"

        # 3. 检查八小对胡法
        if self.eight_pairs_checker is not None:
            can_win_eight, pairs = self.eight_pairs_checker.can_win_eight_pairs(hand)
            if can_win_eight:
                return True, pairs, "八小对"

        return False, [], None

    def _partition_optimized(self, tiles):
        """
        优化的分组算法
        使用剪枝和优先策略提高效率
        """

        # 修复排序：处理万用牌（字符串）和数字的混合
        def sort_key(x):
            if x in SYMBOLS:
                return (0, 0, str(x))  # 符号优先
            elif isinstance(x, str):  # 万用牌
                return (1, 0, x)
            else:  # 数字
                return (2, x, '')

        tiles = sorted(tiles, key=sort_key)
        return self._try_partition_with_pruning(tiles, [])

    def _try_partition_with_pruning(self, remaining, groups):
        """
        带剪枝的递归分组
        优化策略：
        1. 优先尝试刻子（匹配更快）
        2. 使用计数器减少重复计算
        3. 早期剪枝不可能的分支
        """
        # 成功条件
        if len(remaining) == 0:
            return True, groups

        # 剪枝：剩余牌数必须是4的倍数
        if len(remaining) % 4 != 0:
            return False, []

        # 优化1：优先尝试刻子
        counter = Counter(remaining)
        for tile, count in counter.items():
            if count >= 4:
                # 找到刻子，直接使用
                new_remaining = remaining.copy()
                for _ in range(4):
                    new_remaining.remove(tile)

                success, result = self._try_partition_with_pruning(
                    new_remaining,
                    groups + [[tile, tile, tile, tile]]
                )
                if success:
                    return True, result

        # 优化2：尝试算式（从第一张牌开始构建）
        first_tile = remaining[0]

        # 生成包含第一张牌的所有4张组合
        indices = [i for i in range(1, len(remaining))]

        for combo in combinations(indices, 3):
            group = [first_tile] + [remaining[i] for i in combo]

            if self.is_valid_formula(group):
                # 构建剩余牌列表
                used_indices = set([0] + list(combo))
                new_remaining = [remaining[i] for i in range(len(remaining))
                                 if i not in used_indices]

                success, result = self._try_partition_with_pruning(
                    new_remaining,
                    groups + [group]
                )
                if success:
                    return True, result

        return False, []

    def is_ready(self, hand):
        """
        判断给定的牌是否听牌，以及听什么牌（支持万用牌）
        支持：
        - 15张：可以听算术麻将、传统麻将、八小对
        - 11张：只能听算术麻将（3组-1）
        - 7张：只能听算术麻将（2组-1）
        - 3张：只能听算术麻将（1组-1）

        hand: 牌的列表
        返回: (是否听牌, 听牌信息字典)
              听牌信息字典格式: {
                  '算术麻将': [听的牌列表（带标注）],
                  '传统麻将': [听的牌列表],
                  '八小对': [听的牌列表]
              }
        """
        hand_len = len(hand)

        # 检查手牌数量是否合法
        if hand_len not in [15, 11, 7, 3]:
            return False, {}

        ready_info = {}

        # 1. 检查算术麻将听牌（所有手牌数量都支持）
        arith_ready_tiles = set()

        # 扩展搜索范围：包括牌库中没有的20-49的数字
        extended_tiles = self.all_tiles.copy()
        for i in range(20, 50):
            extended_tiles.add(i)

        for tile in extended_tiles:
            test_hand = hand + [tile]
            target_len = hand_len + 1

            if target_len == 16:  # 完整胡牌
                success, _ = self._partition_optimized(test_hand)
                if success:
                    arith_ready_tiles.add(tile)
            elif target_len in [12, 8, 4]:  # 部分组合
                num_groups = target_len // 4
                success, _ = self._partition_optimized_n_groups(test_hand, num_groups)
                if success:
                    arith_ready_tiles.add(tile)

        if arith_ready_tiles:
            # 标注哪些牌需要万用
            annotated_tiles = []
            for tile in sorted(arith_ready_tiles, key=lambda x: (x not in SYMBOLS, x)):
                if tile not in self.tiles_in_pool:
                    # 牌库中不存在，需要标注
                    if isinstance(tile, int) and 20 <= tile <= 49:
                        annotated_tiles.append(f"{tile}（需要万用）")
                    else:
                        annotated_tiles.append(tile)
                else:
                    annotated_tiles.append(tile)
            ready_info['算术麻将'] = annotated_tiles

        # 2. 只有15张牌时才检查传统麻将和八小对
        if hand_len == 15:
            # 检查传统麻将听牌
            if self.traditional_checker is not None:
                is_ready_trad, trad_tiles = self.traditional_checker.is_ready_traditional(hand)
                if is_ready_trad:
                    ready_info['传统麻将'] = sorted(trad_tiles,
                                                    key=lambda x: (x not in SYMBOLS, x))

            # 检查八小对听牌
            if self.eight_pairs_checker is not None:
                is_ready_eight, eight_tiles = self.eight_pairs_checker.is_ready_eight_pairs(hand)
                if is_ready_eight:
                    ready_info['八小对'] = sorted(eight_tiles,
                                                  key=lambda x: (x not in SYMBOLS, x))

        return len(ready_info) > 0, ready_info

    def _partition_optimized_n_groups(self, tiles, n):
        """
        判断能否分成n组有效组合
        tiles: 牌列表
        n: 目标组数
        """
        if len(tiles) != n * 4:
            return False, []

        if n == 1:
            # 只需要一组
            return self.is_valid_group(tiles), [tiles] if self.is_valid_group(tiles) else []

        # 使用优化的分组算法
        def sort_key(x):
            if x in SYMBOLS:
                return (0, 0, str(x))
            elif isinstance(x, str):  # 万用牌
                return (1, 0, x)
            else:  # 数字
                return (2, x, '')

        tiles_sorted = sorted(tiles, key=sort_key)
        return self._try_partition_with_pruning(tiles_sorted, [])

    def format_result(self, success, groups, win_type=None):
        """格式化输出结果"""
        if not success:
            return "无法胡牌"

        if win_type == "传统麻将":
            result = f"可以胡牌！【{win_type}】\n"
            result += f"胡牌组合: {groups}\n"
            return result

        if win_type == "八小对":
            result = f"可以胡牌！【{win_type}】\n"
            result += f"对子组合: {groups}\n"
            return result

        # 算术麻将
        result = f"可以胡牌！【{win_type or '算术麻将'}】分组如下：\n"
        for i, group in enumerate(groups, 1):
            group_str = ' '.join(str(x) for x in group)
            if self.is_kezi(group):
                result += f"第{i}组（刻子）: {group_str}\n"
            else:
                result += f"第{i}组（算式）: {group_str}\n"
        return result


# Re-export parse_hand and format_hand for backward compatibility
# (they are imported from parser module at the top of this file)