"""
算术麻将手牌解析器
集中管理所有牌面常量、符号别名和解析函数
"""

# ============================================================
# 符号常量
# ============================================================

PLUS = '+'
MULTIPLY = '×'
POWER = '∧'

SYMBOLS = {PLUS, MULTIPLY, POWER}

# 符号别名映射（输入 -> 标准符号）
SYMBOL_ALIASES = {
    # 加号
    '+': PLUS,
    '加': PLUS,
    # 乘号
    '*': MULTIPLY,
    'x': MULTIPLY,
    'X': MULTIPLY,
    '×': MULTIPLY,
    '乘': MULTIPLY,
    # 次方
    '^': POWER,
    '∧': POWER,
    '次方': POWER,
    '幂': POWER,
}

# ============================================================
# 胡牌方式别名映射
# ============================================================

WINNING_METHOD_ALIASES = {
    # 自摸
    '自摸': '自摸',
    'tsumo': '自摸',
    'zimo': '自摸',
    'zm': '自摸',
    'z': '自摸',
    # 杠上开花
    '杠上开花': '杠上开花',
    '杠开': '杠上开花',
    '开': '杠上开花',
    'gk': '杠上开花',
    'k': '杠上开花',
    # 海底捞月
    '海底捞月': '海底捞月',
    '海底': '海底捞月',
    '海': '海底捞月',
    'hd': '海底捞月',
    'h': '海底捞月',
    # 抢杠
    '抢杠': '抢杠',
    '抢': '抢杠',
    'qg': '抢杠',
    'q': '抢杠',
    # 天胡
    '天胡': '天胡',
    '天': '天胡',
    'th': '天胡',
    't': '天胡',
    # 点胡
    '点胡': '点胡',
}

# ============================================================
# 万用牌常量
# ============================================================

JOKER_TIAO = 'joker_tiao'    # 条子万用牌（0-9）
JOKER_TONG = 'joker_tong'    # 筒子万用牌（10-19）
JOKER_WAN = 'joker_wan'      # 万字万用牌（20-49）
JOKER_SYMBOL = 'joker_symbol'  # 符号万用牌

JOKERS = {JOKER_TIAO, JOKER_TONG, JOKER_WAN, JOKER_SYMBOL}

# 万用牌别名映射（输入 -> 标准万用牌名）
JOKER_ALIASES = {
    # 条子万用
    'joker_tiao': JOKER_TIAO,
    'jt': JOKER_TIAO,
    '条': JOKER_TIAO,
    '索': JOKER_TIAO,
    '条万用': JOKER_TIAO,
    '索子万用': JOKER_TIAO,
    '条子万用': JOKER_TIAO,
    'ws': JOKER_TIAO,
    'wcs': JOKER_TIAO,
    's': JOKER_TIAO,
    # 筒子万用
    'joker_tong': JOKER_TONG,
    'jtong': JOKER_TONG,
    '筒': JOKER_TONG,
    '饼': JOKER_TONG,
    '筒万用': JOKER_TONG,
    '筒子万用': JOKER_TONG,
    'wp': JOKER_TONG,
    'wcm': JOKER_TONG,
    'p': JOKER_TONG,
    # 万字万用
    'joker_wan': JOKER_WAN,
    'jw': JOKER_WAN,
    '万': JOKER_WAN,
    '万万用': JOKER_WAN,
    '万字万用': JOKER_WAN,
    'wm': JOKER_WAN,
    'wcl': JOKER_WAN,
    'm': JOKER_WAN,
    # 符号万用
    'joker_symbol': JOKER_SYMBOL,
    'js': JOKER_SYMBOL,
    '符': JOKER_SYMBOL,
    '符号': JOKER_SYMBOL,
    '箭': JOKER_SYMBOL,
    '符号万用': JOKER_SYMBOL,
    '风箭万用': JOKER_SYMBOL,
    '箭牌万用': JOKER_SYMBOL,
    'wz': JOKER_SYMBOL,
    'wcop': JOKER_SYMBOL,
    'op': JOKER_SYMBOL,
}

# ============================================================
# 数字牌常量
# ============================================================

# 所有合法的数字牌（根据规则文档）
# 数字牌：0-21, 24, 25, 27, 28, 30, 32, 35, 36, 40, 49
VALID_NUMBER_TILES = (
    set(range(22)) |  # 0-21
    {24, 25, 27, 28, 30, 32, 35, 36, 40, 49}
)

# 所有合法的牌（数字 + 符号）
ALL_TILES = VALID_NUMBER_TILES | SYMBOLS


# ============================================================
# 工具函数
# ============================================================

def tile_sort_key(x):
    """
    麻将牌排序键：符号优先，万用牌次之，数字最后
    
    用于对手牌进行排序，确保分组算法的一致性
    """
    if x in SYMBOLS:
        return (0, 0, str(x))  # 符号优先
    elif isinstance(x, str):  # 万用牌
        return (1, 0, x)
    else:  # 数字
        return (2, x, '')


# ============================================================
# 解析函数
# ============================================================

def parse_hand(hand_str):
    """
    解析手牌字符串，转换为牌列表（支持万用牌）

    支持的输入格式：
    - 数字：直接写数字，用空格或逗号分隔
    - 加号：+
    - 乘号：*, x, X, ×
    - 次方：^, ∧
    - 万用牌：
      - 条子万用：joker_tiao, jt, 条, 索, 条万用, 索子万用
      - 筒子万用：joker_tong, jtong, 筒, 饼, 筒万用, 筒子万用
      - 万字万用：joker_wan, jw, 万, 万万用, 万字万用
      - 符号万用：joker_symbol, js, 符号, 箭, 符号万用, 风箭万用

    示例：
        "1 + 9 10 2 * 3 6 5 5 5 5"
        "1,+,9,10,2,x,3,6,5,5,5,5"
        "1 + 9 10 2 X 3 6 条 5 5 5 ^ ^ ^"
        "1 2 3 4 5 6 筒 7 7 8 8 8 11 11 12 12"

    参数：
        hand_str: 手牌字符串

    返回：
        牌的列表，例如 [1, '+', 9, 10, 2, '×', 3, 6, 'joker_tiao', 5, 5, 5]

    异常：
        ValueError: 无法识别的牌
    """
    # 替换分隔符为空格
    hand_str = hand_str.replace(',', ' ')
    hand_str = hand_str.replace('，', ' ')  # 支持中文逗号

    # 分割成单个token
    tokens = hand_str.split()

    result = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue

        # 检查是否是符号别名
        if token in SYMBOL_ALIASES:
            result.append(SYMBOL_ALIASES[token])
        # 检查是否是万用牌别名
        elif token in JOKER_ALIASES:
            result.append(JOKER_ALIASES[token])
        else:
            # 尝试解析为数字
            try:
                num = int(token)
                result.append(num)
            except ValueError:
                raise ValueError(f"无法识别的牌: '{token}'")

    return result


def format_hand(hand):
    """
    将牌列表格式化为易读的字符串

    参数：
        hand: 牌的列表

    返回：
        格式化的字符串
    """
    return ' '.join(str(tile) for tile in hand)


def validate_tile(tile):
    """
    验证单个牌是否合法

    参数：
        tile: 牌（数字、符号或万用牌）

    返回：
        bool: 是否合法
    """
    if tile in SYMBOLS:
        return True
    if tile in JOKERS:
        return True
    if isinstance(tile, int) and tile in VALID_NUMBER_TILES:
        return True
    return False


def validate_hand(hand, expected_len=None):
    """
    验证手牌是否合法

    参数：
        hand: 牌的列表
        expected_len: 期望的手牌长度（可选）

    返回：
        (bool, str): (是否合法, 错误信息)
    """
    if expected_len is not None and len(hand) != expected_len:
        return False, f"手牌数量错误：期望 {expected_len} 张，实际 {len(hand)} 张"

    for i, tile in enumerate(hand):
        if not validate_tile(tile):
            return False, f"第 {i+1} 张牌不合法: {tile}"

    return True, ""


# ============================================================
# 新增：复杂模式解析函数
# ============================================================

def _normalize_brackets(text: str) -> str:
    """
    统一括号格式：全角转半角
    
    参数：
        text: 输入文本
    
    返回：
        转换后的文本
    """
    # 圆括号
    text = text.replace('（', '(').replace('）', ')')
    # 方括号
    text = text.replace('【', '[').replace('】', ']')
    # 花括号
    text = text.replace('｛', '{').replace('｝', '}')
    return text


def _tokenize_complex(text: str):
    """
    将复杂输入分词成token列表
    保留括号、分隔符等结构信息
    
    参数：
        text: 输入文本
    
    返回：
        token列表
    """
    text = _normalize_brackets(text)
    
    # 替换逗号为空格
    text = text.replace(',', ' ').replace('，', ' ')
    
    tokens = []
    current_token = ''
    
    for char in text:
        if char in '()[]{}|/':
            # 遇到结构字符，先保存当前token
            if current_token.strip():
                tokens.append(current_token.strip())
                current_token = ''
            tokens.append(char)
        elif char in ' \t\n':
            # 遇到空白，保存当前token
            if current_token.strip():
                tokens.append(current_token.strip())
                current_token = ''
        else:
            current_token += char
    
    # 保存最后一个token
    if current_token.strip():
        tokens.append(current_token.strip())
    
    return tokens


def _parse_tile_token(token: str):
    """
    解析单个牌的token，支持d和w后缀
    
    参数：
        token: 牌的token字符串（如 "11d", "12w", "11dw", "11wd", "+", "5"）
    
    返回：
        (value, is_dora, is_joker_used)
        - value: int或str
        - is_dora: bool
        - is_joker_used: bool
    
    异常：
        ValueError: 无法识别的token
    """
    if not token:
        raise ValueError("空token")
    
    is_dora = False
    is_joker_used = False
    
    # 检查后缀（支持 "dw" 和 "wd" 两种顺序）
    # 先统一检查是否包含这两个后缀
    if 'd' in token[-2:]:
        is_dora = True
    if 'w' in token[-2:]:
        is_joker_used = True
    
    # 移除后缀
    if len(token) >= 2 and token[-2:] in ['dw', 'wd']:
        token = token[:-2]
    elif len(token) >= 1 and token[-1] in ['d', 'w']:
        token = token[:-1]
    
    # 检查是否是符号
    if token in SYMBOL_ALIASES:
        return SYMBOL_ALIASES[token], is_dora, is_joker_used
    
    # 检查是否是万用牌
    if token in JOKER_ALIASES:
        return JOKER_ALIASES[token], is_dora, is_joker_used
    
    # 尝试解析为数字
    try:
        value = int(token)
        return value, is_dora, is_joker_used
    except ValueError:
        raise ValueError(f"无法识别的牌token: '{token}'")


def _parse_melded_group(tokens: list, start_idx: int):
    """
    从tokens中解析一个鸣牌面子（圆括号包裹的部分）
    
    参数：
        tokens: token列表
        start_idx: 起始索引（应该是'('）
    
    返回：
        (MeldedGroup, next_idx)
        - MeldedGroup: 解析出的鸣牌面子
        - next_idx: 下一个token的索引
    
    异常：
        ValueError: 解析错误
    """
    from hand_structure import MeldedGroup, Tile, create_tile_from_value
    
    if tokens[start_idx] != '(':
        raise ValueError(f"期望'('，实际'{tokens[start_idx]}'")
    
    # 找到匹配的右括号
    end_idx = start_idx + 1
    depth = 1
    while end_idx < len(tokens) and depth > 0:
        if tokens[end_idx] == '(':
            depth += 1
        elif tokens[end_idx] == ')':
            depth -= 1
        end_idx += 1
    
    if depth != 0:
        raise ValueError("括号不匹配")
    
    # 提取括号内的tokens
    inner_tokens = tokens[start_idx + 1:end_idx - 1]
    
    if not inner_tokens:
        raise ValueError("空的鸣牌面子")
    
    # 检查是否有明/暗标记
    group_type = None
    if inner_tokens[-1] in ['明', '暗']:
        type_marker = inner_tokens[-1]
        inner_tokens = inner_tokens[:-1]
        group_type = 'gang_ming' if type_marker == '明' else 'gang_an'
    
    # 解析牌
    tiles = []
    for token in inner_tokens:
        if token in ['(', ')', '[', ']', '{', '}', '|', '/']:
            raise ValueError(f"鸣牌面子中出现非法字符: '{token}'")
        
        value, is_dora, is_joker_used = _parse_tile_token(token)
        tile = create_tile_from_value(value, is_dora, is_joker_used)
        tiles.append(tile)
    
    # 自动推断面子类型（如果没有明确标记）
    if group_type is None:
        if len(tiles) == 1:
            group_type = 'single_gang'
        elif len(tiles) == 4:
            # 判断是吃还是碰
            if len(set(t.value for t in tiles)) == 1:
                group_type = 'peng'
            else:
                group_type = 'chi'
        elif len(tiles) == 5:
            # 默认暗杠（如果没有标记）
            group_type = 'gang_an'
        else:
            raise ValueError(f"无效的鸣牌面子张数: {len(tiles)}")
    
    melded_group = MeldedGroup(tiles, group_type)
    return melded_group, end_idx


def parse_mode1_already_won(hand_str: str):
    """
    模式1：16张已胡番数模式
    
    格式：(鸣牌) (鸣牌) 手牌算式1 / 手牌算式2 / ... [胡牌] {胡牌方式}
    
    示例：
        "(11d) (2 2 2 2w) (3 + 10 13d) 5 + 7 12w / 9 [+] 5 14 {自摸}"
        "2 0 2 / 2 3 [4] / + + + / * * * / 6 6 / 7 7w"
    
    参数：
        hand_str: 输入字符串
    
    返回：
        Hand对象
    
    异常：
        ValueError: 解析错误
    """
    from hand_structure import Hand, Tile, create_tile_from_value
    
    tokens = _tokenize_complex(hand_str)
    
    melded_groups = []
    hand_groups = []
    current_group = []
    winning_tile = None
    winning_method = None
    winning_tile_in_current = False
    
    idx = 0
    while idx < len(tokens):
        token = tokens[idx]
        
        if token == '(':
            # 解析鸣牌面子
            melded_group, next_idx = _parse_melded_group(tokens, idx)
            melded_groups.append(melded_group)
            idx = next_idx
        
        elif token == '[':
            # 解析胡牌标记
            idx += 1
            if idx >= len(tokens):
                raise ValueError("'['后缺少牌")
            
            winning_token = tokens[idx]
            value, is_dora, is_joker_used = _parse_tile_token(winning_token)
            winning_tile = create_tile_from_value(value, is_dora, is_joker_used)
            
            # 将胡牌加入当前组
            current_group.append(winning_tile)
            winning_tile_in_current = True
            
            idx += 1
            if idx >= len(tokens) or tokens[idx] != ']':
                raise ValueError("缺少']'")
            idx += 1
        
        elif token == '{':
            # 解析胡牌方式
            idx += 1
            if idx >= len(tokens):
                raise ValueError("'{'后缺少胡牌方式")
            
            raw_method = tokens[idx]
            # 标准化胡牌方式（应用别名）
            winning_method = WINNING_METHOD_ALIASES.get(raw_method, raw_method)
            
            idx += 1
            if idx >= len(tokens) or tokens[idx] != '}':
                raise ValueError("缺少'}'")
            idx += 1
        
        elif token in ['|', '/']:
            # 分组分隔符
            if current_group:
                hand_groups.append(current_group)
                current_group = []
                winning_tile_in_current = False
            idx += 1
        
        else:
            # 普通牌
            value, is_dora, is_joker_used = _parse_tile_token(token)
            tile = create_tile_from_value(value, is_dora, is_joker_used)
            current_group.append(tile)
            idx += 1
    
    # 保存最后一组
    if current_group:
        hand_groups.append(current_group)
    
    # 自动推断win_type（根据分组结构）
    win_type = None
    if hand_groups:
        # 检查每组的长度
        group_lengths = [len(group) for group in hand_groups]
        
        # 如果所有组都是4张，那是算术麻将
        if all(length == 4 for length in group_lengths):
            win_type = "算术麻将"
        # 如果有2张一组的，可能是传统麻将或八小对
        elif any(length == 2 for length in group_lengths):
            # 如果都是2张一组，是八小对
            if all(length == 2 for length in group_lengths):
                win_type = "八小对"
            # 否则是传统麻将（有3张和2张混合）
            else:
                win_type = "传统麻将"
        # 如果有3张一组的，是传统麻将
        elif any(length == 3 for length in group_lengths):
            win_type = "传统麻将"
    
    # 创建Hand对象
    hand = Hand(
        melded_groups=melded_groups,
        hand_tiles=[],  # 模式1手牌已经分组，不需要hand_tiles
        hand_groups=hand_groups,
        winning_tile=winning_tile,
        winning_method=winning_method,
        win_type=win_type  # 设置推断出的胡牌类型
    )
    
    # 验证手牌张数
    from hand_validator import validate_hand_count, validate_special_winning
    is_valid, error_msg = validate_hand_count(hand)
    if not is_valid:
        raise ValueError(f"手牌数量错误：{error_msg}")
    
    # 如果没有分组（可能是特殊胜利），需要额外验证
    if not hand_groups or len(hand_groups) == 1:
        # 检查是否为5个特殊胜利之一
        special_types = ["八仙过海", "四仙过海", "天龙", "地龙", "十三幺"]
        is_special = False
        
        for special_type in special_types:
            is_valid_special, _ = validate_special_winning(hand, special_type)
            if is_valid_special:
                is_special = True
                hand.win_type = special_type
                break
        
        # 如果不是特殊胜利，检查能否组成算术麻将/传统麻将/八小对
        if not is_special:
            # 提取所有手牌（不包括鸣牌）
            all_hand_tiles = []
            for group in hand_groups:
                all_hand_tiles.extend([tile.value if hasattr(tile, 'value') else tile for tile in group])
            
            # 检查能否组成有效分组
            from hand_validator import can_form_valid_groups
            if len(all_hand_tiles) == 16 and not can_form_valid_groups(all_hand_tiles):
                raise ValueError("诈胡：手牌既不满足特殊胜利条件，也无法组成有效的算术麻将/传统麻将/八小对")
    
    return hand


def parse_mode2_check_win(hand_str: str):
    """
    模式2：16张是否胡模式
    
    格式：(鸣牌) (鸣牌) 手牌（未分组） [胡牌]
    
    示例：
        "(11d) (2 2 2 2w) (3 + 10 13d) 5 7 wp 9 5 14 + [+]"
    
    参数：
        hand_str: 输入字符串
    
    返回：
        Hand对象
    
    异常：
        ValueError: 解析错误
    """
    from hand_structure import Hand, create_tile_from_value
    
    tokens = _tokenize_complex(hand_str)
    
    melded_groups = []
    hand_tiles = []
    winning_tile = None
    
    idx = 0
    while idx < len(tokens):
        token = tokens[idx]
        
        if token == '(':
            # 解析鸣牌面子
            melded_group, next_idx = _parse_melded_group(tokens, idx)
            melded_groups.append(melded_group)
            idx = next_idx
        
        elif token == '[':
            # 解析胡牌标记
            idx += 1
            if idx >= len(tokens):
                raise ValueError("'['后缺少牌")
            
            winning_token = tokens[idx]
            value, is_dora, is_joker_used = _parse_tile_token(winning_token)
            winning_tile = create_tile_from_value(value, is_dora, is_joker_used)
            
            # 也加入手牌（因为是16张总数的一部分）
            hand_tiles.append(winning_tile)
            
            idx += 1
            if idx >= len(tokens) or tokens[idx] != ']':
                raise ValueError("缺少']'")
            idx += 1
        
        elif token in ['|', '/', '{', '}']:
            # 模式2不应该有这些符号
            raise ValueError(f"模式2中出现非法符号: '{token}'")
        
        else:
            # 普通牌
            value, is_dora, is_joker_used = _parse_tile_token(token)
            tile = create_tile_from_value(value, is_dora, is_joker_used)
            hand_tiles.append(tile)
            idx += 1
    
    # 创建Hand对象
    hand = Hand(
        melded_groups=melded_groups,
        hand_tiles=hand_tiles,
        winning_tile=winning_tile
    )
    
    return hand


def parse_mode3_ready_with_meld(hand_str: str):
    """
    模式3：有鸣牌听牌模式（15张）
    
    格式：(鸣牌) (鸣牌) 手牌（未分组）
    
    示例：
        "(11d) (2 2 2 2w) (3 + 10 13d) 5 7 wp 9 5 14 +"
    
    参数：
        hand_str: 输入字符串
    
    返回：
        Hand对象
    
    异常：
        ValueError: 解析错误
    """
    from hand_structure import Hand, create_tile_from_value
    
    tokens = _tokenize_complex(hand_str)
    
    melded_groups = []
    hand_tiles = []
    
    idx = 0
    while idx < len(tokens):
        token = tokens[idx]
        
        if token == '(':
            # 解析鸣牌面子
            melded_group, next_idx = _parse_melded_group(tokens, idx)
            melded_groups.append(melded_group)
            idx = next_idx
        
        elif token in ['[', ']', '{', '}', '|', '/']:
            # 模式3不应该有这些符号
            raise ValueError(f"模式3中出现非法符号: '{token}'")
        
        else:
            # 普通牌
            value, is_dora, is_joker_used = _parse_tile_token(token)
            tile = create_tile_from_value(value, is_dora, is_joker_used)
            hand_tiles.append(tile)
            idx += 1
    
    # 创建Hand对象
    hand = Hand(
        melded_groups=melded_groups,
        hand_tiles=hand_tiles
    )
    
    return hand


def parse_mode4_ready_no_meld(hand_str: str):
    """
    模式4：无鸣牌听牌模式（15张）
    
    格式：手牌（未分组，无圆括号）
    
    这实际上就是原有的 parse_hand 函数，但为了统一接口，
    我们将其转换为Hand对象返回。
    
    示例：
        "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15"
    
    参数：
        hand_str: 输入字符串
    
    返回：
        Hand对象
    
    异常：
        ValueError: 解析错误
    """
    from hand_structure import Hand, create_tile_from_value
    
    # 使用原有的parse_hand函数
    simple_tiles = parse_hand(hand_str)
    
    # 转换为Tile对象
    hand_tiles = []
    for tile_value in simple_tiles:
        # 模式4中的牌都是普通牌，没有d或w标记
        tile = create_tile_from_value(tile_value, False, False)
        hand_tiles.append(tile)
    
    # 创建Hand对象
    hand = Hand(
        melded_groups=[],
        hand_tiles=hand_tiles
    )
    
    return hand
