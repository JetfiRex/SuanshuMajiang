from itertools import combinations, product
from collections import Counter

from parser import (
    PLUS, MULTIPLY, POWER, SYMBOLS,
    JOKER_TIAO, JOKER_TONG, JOKER_WAN, JOKER_SYMBOL, JOKERS,
    ALL_TILES,
    parse_hand, format_hand, tile_sort_key,
    parse_mode1_already_won
)

# 导入传统麻将和八小对判定器
try:
    from traditional_mahjong import TraditionalMahjongChecker, EightPairsChecker
    TRADITIONAL_AVAILABLE = True
except ImportError:
    TRADITIONAL_AVAILABLE = False
    print("警告: 未找到 traditional_mahjong.py，传统麻将和八小对功能将不可用")

# 导入番数计算器
try:
    from fan_calculator import calculate_fan, format_fan_result
    FAN_CALCULATOR_AVAILABLE = True
except ImportError:
    FAN_CALCULATOR_AVAILABLE = False
    print("警告: 未找到 fan_calculator.py，番数计算功能将不可用")

# 导入空听检查模块
try:
    from empty_listening_checker import analyze_ready_tiles, format_ready_tiles_with_status
    EMPTY_LISTENING_AVAILABLE = True
except ImportError:
    EMPTY_LISTENING_AVAILABLE = False
    # 空听检查是可选功能，不需要警告


class ArithmeticMahjong:
    """算术麻将胡牌判定器（支持万用牌和番数计算）"""

    def __init__(self, require_sum_gte_10=True, min_fan=None):
        """
        初始化算术麻将判定器

        参数:
            require_sum_gte_10: bool, 是否要求加法算式的和必须>=10
                               True: 进阶规则，加法和必须>=10，起胡8番（默认）
                               False: 新手规则，加法和可以<10，起胡0番
            min_fan: int, 起胡番数（可选，如果不指定则根据规则自动设置）
        """
        # 使用 parser 模块的常量
        self.symbols = SYMBOLS

        # 规则设置
        self.require_sum_gte_10 = require_sum_gte_10
        
        # 起胡番数：如果指定了min_fan则使用指定值，否则根据规则设置
        if min_fan is not None:
            self.min_fan = min_fan
        else:
            # 新手规则：0番起胡；进阶规则：8番起胡
            self.min_fan = 8 if require_sum_gte_10 else 0

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

    def can_win(self, hand, winning_method=None, has_melded=False):
        """
        判断给定的牌是否能胡牌
        会检查：
        1. 16张：标准算术麻将胡法（4组算式/刻子，4+4+4+4）
        2. 16张：传统麻将胡法（4组面子+2对将，3+3+3+3+2+2）
           - 但如果有鸣牌（has_melded=True），不检查传统麻将
           - 如果既能算术又能传统，计算两种番数，返回番数更高的
        3. 14张：传统麻将胡法或八小对胡法
        
        并计算番数（如果可用）

        hand: 牌的列表，例如 [1, 2, 3, '+', 5, 5, 5, 5, ...]
        winning_method: 胡牌方式（可选），如 '自摸', '抢杠', '杠上开花' 等
        has_melded: 是否有鸣牌（如果有，不检查传统麻将）
        
        返回: (是否能胡, 分组方案, 胡牌类型, 番数信息)
              番数信息格式: {
                  'total_fan': 总番数,
                  'fan_result': FanResults对象（如果番数计算可用）,
                  'can_start': 是否满足起胡条件
              }
        """
        hand_len = len(hand)
        
        # 算术麻将：16张
        if hand_len == 16:
            # 收集所有可能的胡法及其番数
            win_options = []  # [(win_type, groups, fan_info), ...]
            
            # 1. 检查算术麻将胡法（4+4+4+4）
            can_win_arith, groups_arith = self._partition_optimized(hand)
            if can_win_arith:
                fan_info_arith = self._calculate_fan(hand, groups_arith, "算术麻将", winning_method)
                win_options.append(("算术麻将", groups_arith, fan_info_arith))
            
            # 2. 如果没有鸣牌，检查传统麻将（3+3+3+3+2+2）
            if not has_melded and self.traditional_checker is not None:
                can_win_trad, groups_trad = self.traditional_checker.can_win_traditional(hand)
                if can_win_trad:
                    fan_info_trad = self._calculate_fan(hand, groups_trad, "传统麻将", winning_method)
                    win_options.append(("传统麻将", groups_trad, fan_info_trad))
            
            # 3. 检查八小对（2+2+2+2+2+2+2+2）- 16张！
            if self.eight_pairs_checker is not None:
                can_win_eight, pairs = self.eight_pairs_checker.can_win_eight_pairs(hand)
                if can_win_eight:
                    fan_info_eight = self._calculate_fan(hand, pairs, "八小对", winning_method)
                    win_options.append(("八小对", pairs, fan_info_eight))
            
            # 4. 如果有多个可能的胡法，选择最优的
            if len(win_options) > 0:
                # 筛选满足起胡条件的胡法
                valid_options = [opt for opt in win_options 
                                if opt[2] and opt[2]['total_fan'] >= self.min_fan]
                
                if valid_options:
                    # 如果有满足起胡的，选择番数最高的
                    valid_options.sort(key=lambda x: x[2]['total_fan'], reverse=True)
                    best_win_type, best_groups, best_fan_info = valid_options[0]
                    return True, best_groups, best_win_type, best_fan_info
                else:
                    # 如果都不满足起胡，返回不能胡
                    return False, [], None, None
            
            return False, [], None, None
        
        # 传统麻将和八小对：14张
        elif hand_len == 14:
            # 收集所有可能的胡法及其番数
            win_options = []
            
            # 检查传统麻将胡法
            if self.traditional_checker is not None:
                can_win_trad, result_trad = self.traditional_checker.can_win_traditional(hand)
                if can_win_trad:
                    fan_info_trad = self._calculate_fan(hand, result_trad, "传统麻将", winning_method)
                    win_options.append(("传统麻将", result_trad, fan_info_trad))
            
            # 检查八小对胡法（7对）
            if self.eight_pairs_checker is not None:
                can_win_eight, pairs = self.eight_pairs_checker.can_win_eight_pairs(hand)
                if can_win_eight:
                    fan_info_eight = self._calculate_fan(hand, pairs, "八小对", winning_method)
                    win_options.append(("八小对", pairs, fan_info_eight))
            
            # 选择最优的胡法
            if len(win_options) > 0:
                # 筛选满足起胡条件的胡法
                valid_options = [opt for opt in win_options 
                                if opt[2] and opt[2]['total_fan'] >= self.min_fan]
                
                if valid_options:
                    # 如果有满足起胡的，选择番数最高的
                    valid_options.sort(key=lambda x: x[2]['total_fan'], reverse=True)
                    best_win_type, best_groups, best_fan_info = valid_options[0]
                    return True, best_groups, best_win_type, best_fan_info
                else:
                    # 如果都不满足起胡，返回不能胡
                    return False, [], None, None
            
            return False, [], None, None
        
        else:
            # 其他张数都不能胡牌
            return False, [], None, None

    def _calculate_fan(self, hand, groups, win_type, winning_method=None):
        """
        计算番数
        
        返回番数信息字典
        """
        if not FAN_CALCULATOR_AVAILABLE:
            return None
        
        try:
            # 构建模式1的输入字符串来调用番数计算器
            # 格式：formula1 / formula2 / formula3 / formula4
            hand_str = self._build_mode1_string(hand, groups, win_type, winning_method)
            
            if hand_str:
                hand_obj = parse_mode1_already_won(hand_str)
                # 设置win_type，防止番数计算时违反不拆移原则
                hand_obj.win_type = win_type
                fan_result = calculate_fan(hand_obj, min_fan=self.min_fan)
                
                return {
                    'total_fan': fan_result.get_total_fan(),
                    'fan_result': fan_result,
                    'can_start': fan_result.get_total_fan() >= self.min_fan
                }
        except Exception as e:
            print(f"番数计算出错: {e}")
        
        return None
    
    def _format_traditional_group(self, group):
        """
        将传统麻将的元组格式转换为可读字符串
        
        例如：
        ('将', ('箭', '中'), ('箭', '中')) → "红中 红中"
        ('刻子', ('条', 2), ('条', 2), ('条', 2)) → "2 2 2"
        ('顺子', ('筒', 7), ('筒', 8), ('筒', 9)) → "17 18 19"
        """
        # 特殊牌名映射
        special_names = {
            ('风', '东'): '东风',
            ('风', '南'): '南风',
            ('风', '西'): '西风',
            ('风', '北'): '北风',
            ('箭', '中'): '红中',
            ('箭', '发'): '发财',
            ('箭', '白'): '白板',
        }
        
        # 数字到算术麻将的映射
        tile_map = {
            ('条', i): str(i) for i in range(1, 10)
        }
        tile_map.update({
            ('筒', i): str(10 + i) for i in range(1, 10)
        })
        # 万子映射
        wan_map = {
            1: 21, 2: 32, 3: 35, 4: 24, 5: 25,
            6: 36, 7: 27, 8: 28, 9: 49
        }
        tile_map.update({
            ('万', i): str(wan_map[i]) for i in range(1, 10)
        })
        
        # 风牌和箭牌
        tile_map.update(special_names)
        
        # 符号映射
        tile_map[('箭', '中')] = '+'
        tile_map[('箭', '发')] = '×'
        tile_map[('箭', '白')] = '∧'
        
        # 跳过第一个元素（'将'/'刻子'/'顺子'），转换剩余的牌
        tiles_str = []
        for tile_tuple in group[1:]:
            if tile_tuple in tile_map:
                tiles_str.append(tile_map[tile_tuple])
            else:
                # 如果映射表中没有，尝试直接用数字
                tiles_str.append(str(tile_tuple[1]))
        
        return ' '.join(tiles_str)
    
    def _format_tile_for_display(self, tile):
        """
        格式化单张牌的显示
        
        如果是万用牌代替的，显示"原值(代替为当前值)"或"万用类型(代替为当前值)"
        如果有宝牌标记，保留'd'后缀
        """
        if isinstance(tile, str):
            return str(tile)
        
        # 检查是否是Tile对象
        if hasattr(tile, 'value'):
            value_str = str(tile.value)
            
            # 如果是万用牌代替的
            if hasattr(tile, 'is_joker_used') and tile.is_joker_used:
                joker_type_names = {
                    'tiao': '条万用',
                    'tong': '筒万用',
                    'wan': '万万用',
                    'symbol': '符号万用',
                    None: '万用'
                }
                joker_name = joker_type_names.get(tile.joker_type, '万用')
                
                # 特殊处理：如果原值是0，显示"0(代替为X)"
                if tile.value == 0:
                    value_str = f"0(代替为{tile.value})"
                else:
                    value_str = f"{joker_name}(代替为{tile.value})"
            
            # 添加宝牌后缀
            if hasattr(tile, 'is_dora') and tile.is_dora:
                value_str += 'd'
            
            return value_str
        
        return str(tile)
    
    def _format_groups_for_display(self, groups, win_type):
        """
        格式化分组以便显示
        
        返回格式：
        - 算术麻将：直接用 / 分隔各组
        - 传统麻将：转换为可读格式后用 / 分隔
        """
        if win_type == "算术麻将" or win_type == "算术麻将（部分）":
            # 算术麻将：显示Tile对象，保留万用牌和宝牌标记
            group_strs = []
            for group in groups:
                tiles_str = []
                for tile in group:
                    tiles_str.append(self._format_tile_for_display(tile))
                group_strs.append(' '.join(tiles_str))
            return ' / '.join(group_strs)
        
        elif win_type in ["传统麻将", "八小对"]:
            # 传统麻将：需要转换元组格式
            group_strs = []
            for group in groups:
                if isinstance(group, tuple) and len(group) > 0:
                    # 传统麻将格式
                    group_str = self._format_traditional_group(group)
                    group_strs.append(group_str)
                elif isinstance(group, list):
                    # 如果是Tile对象列表
                    tiles_str = []
                    for tile in group:
                        tiles_str.append(self._format_tile_for_display(tile))
                    group_strs.append(' '.join(tiles_str))
                else:
                    # 其他格式
                    tiles = ' '.join(str(tile) for tile in group)
                    group_strs.append(tiles)
            return ' / '.join(group_strs)
        
        else:
            # 其他类型
            group_strs = []
            for group in groups:
                if isinstance(group, list):
                    tiles_str = []
                    for tile in group:
                        tiles_str.append(self._format_tile_for_display(tile))
                    group_strs.append(' '.join(tiles_str))
                else:
                    tiles = ' '.join(str(tile) for tile in group)
                    group_strs.append(tiles)
            return ' / '.join(group_strs)

    def _build_mode1_string(self, hand, groups, win_type, winning_method=None):
        """
        根据胡牌信息构建模式1输入字符串
        """
        # 传统麻将牌面到算术麻将的反向映射
        tile_to_num = {
            # 条子 1-9
            ('条', 1): '1', ('条', 2): '2', ('条', 3): '3', ('条', 4): '4', ('条', 5): '5',
            ('条', 6): '6', ('条', 7): '7', ('条', 8): '8', ('条', 9): '9',
            # 筒子 11-19
            ('筒', 1): '11', ('筒', 2): '12', ('筒', 3): '13', ('筒', 4): '14', ('筒', 5): '15',
            ('筒', 6): '16', ('筒', 7): '17', ('筒', 8): '18', ('筒', 9): '19',
            # 万子
            ('万', 1): '21', ('万', 2): '32', ('万', 3): '35', ('万', 4): '24', ('万', 5): '25',
            ('万', 6): '36', ('万', 7): '27', ('万', 8): '28', ('万', 9): '49',
            # 风牌
            ('风', '北'): '10', ('风', '南'): '20', ('风', '东'): '30', ('风', '西'): '40',
            # 箭牌（符号）
            ('箭', '中'): '+', ('箭', '发'): '×', ('箭', '白'): '∧',
        }
        
        # 将分组转换为字符串
        group_strs = []
        for group in groups:
            # 检查是否是八小对的格式：(tile, tile) 二元组
            if isinstance(group, tuple) and len(group) == 2:
                # 检查是否都是数字或'joker'
                if (isinstance(group[0], int) or group[0] == 'joker') and \
                   (isinstance(group[1], int) or group[1] == 'joker'):
                    # 八小对格式：(2, 2) 或 (15, 'joker')
                    tiles_in_group = []
                    for item in group:
                        if item == 'joker':
                            tiles_in_group.append('0')  # 万用牌用0表示
                        else:
                            tiles_in_group.append(str(item))
                    group_str = ' '.join(tiles_in_group)
                    group_strs.append(group_str)
                    continue
            
            # 检查是否是传统麻将的格式（元组形式）
            if len(group) > 0 and isinstance(group, tuple):
                # 传统麻将格式：('将', ('条', 2), ('条', 2)) 或 ('顺', ('条', 2), ('条', 3), ('条', 4))
                # 跳过第一个标记（'将'/'刻'/'顺'），只保留牌
                tiles_in_group = []
                for item in group[1:]:
                    # 每个牌也是元组：('条', 2) 或 ('筒', 5) 或 ('箭', '发')
                    if isinstance(item, tuple) and len(item) == 2:
                        # 使用反向映射转换
                        if item in tile_to_num:
                            tiles_in_group.append(tile_to_num[item])
                        else:
                            # 如果映射表中没有，尝试直接用数字
                            tiles_in_group.append(str(item[1]))
                    else:
                        # 如果不是元组格式，直接转字符串
                        tiles_in_group.append(str(item))
                group_str = ' '.join(tiles_in_group)
            else:
                # 算术麻将格式：[tile1, tile2, tile3, tile4]
                group_str = ' '.join(str(tile) for tile in group)
            group_strs.append(group_str)
        
        # 组合成模式1格式
        result = ' / '.join(group_strs)
        
        # 添加胡牌方式（如果提供）
        if winning_method:
            result += f" {{{winning_method}}}"
        
        return result

    def _partition_optimized(self, tiles):
        """
        优化的分组算法
        使用剪枝和优先策略提高效率
        """
        tiles = sorted(tiles, key=tile_sort_key)
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

    def is_ready(self, hand, return_details=False):
        """
        判断给定的牌是否听牌，以及听什么牌（支持万用牌）
        支持：
        - 15张：可以听算术麻将、传统麻将、八小对
        - 11张：只能听算术麻将（3组-1）
        - 7张：只能听算术麻将（2组-1）
        - 3张：只能听算术麻将（1组-1）

        hand: 牌的列表
        return_details: 是否返回详细信息（包括牌型组合和番数）
        
        返回: (是否听牌, 听牌信息字典)
        
        如果return_details=False（默认）：
              听牌信息字典格式: {
                  '算术麻将': [听的牌列表（带标注）],
                  '传统麻将': [听的牌列表],
                  '八小对': [听的牌列表]
              }
        
        如果return_details=True：
              听牌信息字典格式: {
                  '算术麻将': {
                      'tiles': [听的牌列表],
                      'details': {
                          tile: {
                              'groups': [胡牌组合],
                              'win_type': '算术麻将',
                              'fan_info': {番数信息} or None
                          }
                      }
                  },
                  '传统麻将': { ... },
                  '八小对': { ... }
              }
        """
        hand_len = len(hand)

        # 检查手牌数量是否合法
        if hand_len not in [15, 11, 7, 3]:
            return False, {}

        ready_info = {}

        # 1. 检查算术麻将听牌（所有手牌数量都支持）
        arith_ready_tiles = set()
        arith_details = {}  # 存储详细信息

        # 扩展搜索范围：包括牌库中没有的20-49的数字
        extended_tiles = self.all_tiles.copy()
        for i in range(20, 50):
            extended_tiles.add(i)

        for tile in extended_tiles:
            test_hand = hand + [tile]
            target_len = hand_len + 1

            if target_len == 16:  # 完整胡牌
                success, groups = self._partition_optimized(test_hand)
                if success:
                    arith_ready_tiles.add(tile)
                    if return_details:
                        # 计算番数
                        fan_info = self._calculate_fan(test_hand, groups, "算术麻将", None)
                        arith_details[tile] = {
                            'groups': groups,
                            'win_type': '算术麻将',
                            'fan_info': fan_info
                        }
            elif target_len in [12, 8, 4]:  # 部分组合
                num_groups = target_len // 4
                success, groups = self._partition_optimized_n_groups(test_hand, num_groups)
                if success:
                    arith_ready_tiles.add(tile)
                    if return_details:
                        # 部分组合暂不计算番数
                        arith_details[tile] = {
                            'groups': groups,
                            'win_type': '算术麻将（部分）',
                            'fan_info': None
                        }

        if arith_ready_tiles:
            if return_details:
                # 返回详细信息
                ready_info['算术麻将'] = {
                    'tiles': sorted(list(arith_ready_tiles), key=lambda x: (x not in SYMBOLS, x)),
                    'details': arith_details
                }
            else:
                # 使用空听检查模块分析听牌状态
                if EMPTY_LISTENING_AVAILABLE:
                    analysis = analyze_ready_tiles(list(arith_ready_tiles), hand)
                    # 按状态分组显示
                    annotated_tiles = []
                    for tile in sorted(arith_ready_tiles, key=lambda x: (x not in SYMBOLS, x)):
                        if tile in analysis:
                            annotated_tiles.append(analysis[tile]['display'])
                        else:
                            annotated_tiles.append(str(tile))
                    ready_info['算术麻将'] = annotated_tiles
                else:
                    # 降级方案：只标注需要万用的牌（不检查空听）
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
                    if return_details:
                        trad_details = {}
                        for tile in trad_tiles:
                            test_hand = hand + [tile]
                            can_win_trad, groups_trad = self.traditional_checker.can_win_traditional(test_hand)
                            if can_win_trad:
                                fan_info = self._calculate_fan(test_hand, groups_trad, "传统麻将", None)
                                trad_details[tile] = {
                                    'groups': groups_trad,
                                    'win_type': '传统麻将',
                                    'fan_info': fan_info
                                }
                        ready_info['传统麻将'] = {
                            'tiles': sorted(trad_tiles, key=lambda x: (x not in SYMBOLS, x)),
                            'details': trad_details
                        }
                    else:
                        ready_info['传统麻将'] = sorted(trad_tiles,
                                                        key=lambda x: (x not in SYMBOLS, x))

            # 检查八小对听牌
            if self.eight_pairs_checker is not None:
                is_ready_eight, eight_tiles = self.eight_pairs_checker.is_ready_eight_pairs(hand)
                if is_ready_eight:
                    if return_details:
                        eight_details = {}
                        for tile in eight_tiles:
                            test_hand = hand + [tile]
                            can_win_eight, groups_eight = self.eight_pairs_checker.can_win_eight_pairs(test_hand)
                            if can_win_eight:
                                fan_info = self._calculate_fan(test_hand, groups_eight, "八小对", None)
                                eight_details[tile] = {
                                    'groups': groups_eight,
                                    'win_type': '八小对',
                                    'fan_info': fan_info
                                }
                        ready_info['八小对'] = {
                            'tiles': sorted(eight_tiles, key=lambda x: (x not in SYMBOLS, x)),
                            'details': eight_details
                        }
                    else:
                        ready_info['八小对'] = sorted(eight_tiles,
                                                      key=lambda x: (x not in SYMBOLS, x))

        return len(ready_info) > 0, ready_info

    def display_ready_interactive(self, hand):
        """
        交互式显示听牌信息
        
        第一步：显示听牌列表和每张牌的总番数
        第二步：询问是否需要详细信息
        第三步：如果选择y，显示详细的胡法和番种构成
        """
        # 获取详细信息
        is_ready, ready_info = self.is_ready(hand, return_details=True)
        
        if not is_ready:
            print("不听牌")
            return
        
        # 第一步：显示简要信息
        print("=" * 70)
        print("听牌信息")
        print("=" * 70)
        
        for win_type, info in ready_info.items():
            print(f"\n【{win_type}】")
            
            # 按番数排序
            tiles_with_fan = []
            for tile in info['tiles']:
                detail = info['details'].get(tile)
                if detail and detail['fan_info']:
                    fan = detail['fan_info']['total_fan']
                    can_start = detail['fan_info']['can_start']
                    tiles_with_fan.append((tile, fan, can_start))
                else:
                    tiles_with_fan.append((tile, None, False))
            
            # 显示听牌和番数
            for tile, fan, can_start in tiles_with_fan:
                if fan is not None:
                    status = "✅" if can_start else "❌"
                    print(f"  听 {tile:>3}: {fan:>2}番 {status}")
                else:
                    print(f"  听 {tile:>3}: N/A（部分组合）")
        
        # 第二步：询问是否需要详细信息
        print("\n" + "=" * 70)
        choice = input("是否需要查看详细信息（胡法和番种构成）？(y/n): ").strip().lower()
        
        if choice != 'y':
            return
        
        # 第三步：显示详细信息
        print("\n" + "=" * 70)
        print("详细信息")
        print("=" * 70)
        
        for win_type, info in ready_info.items():
            print(f"\n【{win_type}】")
            
            for tile in info['tiles']:
                detail = info['details'].get(tile)
                if not detail:
                    continue
                
                print(f"\n  ━━ 听 {tile} ━━")
                
                # 显示胡法（分组）
                if detail['groups']:
                    formatted_groups = self._format_groups_for_display(
                        detail['groups'], 
                        detail['win_type']
                    )
                    print(f"  胡法: {formatted_groups}")
                
                # 显示番数信息
                if detail['fan_info']:
                    fan_info = detail['fan_info']
                    print(f"  总番数: {fan_info['total_fan']}番")
                    print(f"  满足起胡: {'是' if fan_info['can_start'] else '否'}")
                    
                    # 显示番种构成
                    print(f"  番种构成:")
                    for fan_result in fan_info['fan_result'].results:
                        print(f"    • {fan_result}")
                else:
                    print(f"  番数: N/A（部分组合）")
        
        print("\n" + "=" * 70)

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

        tiles_sorted = sorted(tiles, key=tile_sort_key)
        return self._try_partition_with_pruning(tiles_sorted, [])

    def format_result(self, success, groups, win_type=None, fan_info=None):
        """格式化输出结果（包括番数）"""
        if not success:
            return "无法胡牌"

        if win_type == "传统麻将":
            result = f"可以胡牌！【{win_type}】\n"
            result += f"胡牌组合: {groups}\n"
            if fan_info:
                result += self._format_fan_info(fan_info)
            return result

        if win_type == "八小对":
            result = f"可以胡牌！【{win_type}】\n"
            result += f"对子组合: {groups}\n"
            if fan_info:
                result += self._format_fan_info(fan_info)
            return result

        # 算术麻将
        result = f"可以胡牌！【{win_type or '算术麻将'}】分组如下：\n"
        for i, group in enumerate(groups, 1):
            group_str = ' '.join(str(x) for x in group)
            if self.is_kezi(group):
                result += f"第{i}组（刻子）: {group_str}\n"
            else:
                result += f"第{i}组（算式）: {group_str}\n"
        
        # 添加番数信息
        if fan_info:
            result += self._format_fan_info(fan_info)
        
        return result
    
    def _format_fan_info(self, fan_info):
        """格式化番数信息"""
        if not fan_info:
            return ""
        
        result = "\n" + "=" * 60 + "\n"
        result += f"总番数: {fan_info['total_fan']}番\n"
        
        if fan_info['can_start']:
            result += "✅ 满足起胡条件（8番起胡）\n"
        else:
            result += f"❌ 不满足起胡条件（需要8番，当前{fan_info['total_fan']}番）\n"
        
        if fan_info.get('fan_result'):
            result += "-" * 60 + "\n"
            result += "番种明细:\n"
            for fan in fan_info['fan_result'].results:
                result += f"  {fan}\n"
        
        result += "=" * 60 + "\n"
        
        return result


# Re-export parse_hand and format_hand for backward compatibility
# (they are imported from parser module at the top of this file)
