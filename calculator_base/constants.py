
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