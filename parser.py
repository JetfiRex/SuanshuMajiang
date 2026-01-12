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
