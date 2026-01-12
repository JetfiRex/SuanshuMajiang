"""
算术麻将胡牌判定器测试
使用 pytest 框架
"""

import pytest
from mahjong_checker import ArithmeticMahjong
from parser import parse_hand, format_hand


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def standard_mahjong():
    """标准规则：加法和必须>=10"""
    return ArithmeticMahjong(require_sum_gte_10=True)


@pytest.fixture
def newbie_mahjong():
    """新手规则：加法和可以<10"""
    return ArithmeticMahjong(require_sum_gte_10=False)


# ============================================================
# 解析器测试 (TestParseHand)
# ============================================================

class TestParseHand:
    """测试手牌解析功能"""

    def test_space_separated(self):
        """测试空格分隔的输入"""
        hand_str = "1 + 9 10 2 * 3 6 5 5 5 5 ^ ^ ^ ^"
        hand = parse_hand(hand_str)
        assert hand == [1, '+', 9, 10, 2, '×', 3, 6, 5, 5, 5, 5, '∧', '∧', '∧', '∧']

    def test_comma_separated(self):
        """测试逗号分隔的输入"""
        hand_str = "1,+,9,10,2,x,3,6,5,5,5,5,^,^,^,^"
        hand = parse_hand(hand_str)
        assert hand == [1, '+', 9, 10, 2, '×', 3, 6, 5, 5, 5, 5, '∧', '∧', '∧', '∧']

    @pytest.mark.parametrize("multiply_char", ["*", "x", "X", "×"])
    def test_multiply_symbol_variations(self, multiply_char):
        """测试乘号的不同表示方式"""
        hand_str = f"2 {multiply_char} 3 6"
        hand = parse_hand(hand_str)
        assert hand == [2, '×', 3, 6]

    @pytest.mark.parametrize("power_char", ["^", "∧"])
    def test_power_symbol_variations(self, power_char):
        """测试次方符号的不同表示方式"""
        hand_str = f"2 {power_char} 3 8"
        hand = parse_hand(hand_str)
        assert hand == [2, '∧', 3, 8]

    @pytest.mark.parametrize("joker_input,expected", [
        ("条", "joker_tiao"),
        ("索", "joker_tiao"),
        ("jt", "joker_tiao"),
        ("筒", "joker_tong"),
        ("饼", "joker_tong"),
        ("jtong", "joker_tong"),
        ("万", "joker_wan"),
        ("jw", "joker_wan"),
        ("符号", "joker_symbol"),
        ("箭", "joker_symbol"),
        ("js", "joker_symbol"),
    ])
    def test_joker_aliases(self, joker_input, expected):
        """测试万用牌的多种简写方式"""
        hand = parse_hand(joker_input)
        assert hand == [expected]

    def test_format_hand(self):
        """测试手牌格式化输出"""
        hand = [1, '+', 9, 10, 2, '×', 3, 6, 5, 5, 5, 5, '∧', '∧', '∧', '∧']
        formatted = format_hand(hand)
        assert formatted == "1 + 9 10 2 × 3 6 5 5 5 5 ∧ ∧ ∧ ∧"


# ============================================================
# 算术麻将胡牌测试 (TestArithmeticMahjongWin)
# ============================================================

class TestArithmeticMahjongWin:
    """测试算术麻将胡牌判定"""

    def test_valid_16_tile_win(self, standard_mahjong):
        """测试16张牌的有效胡牌（算术麻将）"""
        hand_str = "1 + 9 10 2 * 3 6 5 5 5 5 ^ ^ ^ ^"
        hand = parse_hand(hand_str)
        can_win, groups, win_type = standard_mahjong.can_win(hand)
        assert can_win is True
        assert win_type == "算术麻将"

    def test_with_joker_tiao_parsing(self, standard_mahjong):
        """测试带条子万用牌的解析（原测试8，15张，用于演示解析）"""
        # 注：原测试中注释写"16张"但实际是15张，结果是"无法胡牌"
        # 这个测试验证joker解析正常工作
        hand_str = "1 + 9 10 2 x 3 6 5 5 5 5 条 ^ ^"
        hand = parse_hand(hand_str)
        assert len(hand) == 15
        assert "joker_tiao" in hand




# ============================================================
# 传统麻将胡牌测试 (TestTraditionalMahjongWin)
# ============================================================

class TestTraditionalMahjongWin:
    """测试传统麻将胡牌判定"""

    def test_valid_16_tile_win(self, standard_mahjong):
        """测试16张牌的有效胡牌（传统麻将）"""
        hand_str = "1 2 3 4 5 6 7 7 7 8 8 8 11 11 12 12"
        hand = parse_hand(hand_str)
        can_win, groups, win_type = standard_mahjong.can_win(hand)
        assert can_win is True
        assert win_type == "传统麻将"

    def test_eight_pairs_win(self, standard_mahjong):
        """测试八小对胡牌"""
        hand_str = "1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8"
        hand = parse_hand(hand_str)
        can_win, groups, win_type = standard_mahjong.can_win(hand)
        assert can_win is True

    def test_with_joker_tong(self, standard_mahjong):
        """测试带筒子万用牌的传统麻将"""
        hand_str = "1 2 3 4 5 6 7 7 7 8 8 8 11 11 12 筒"
        hand = parse_hand(hand_str)
        can_win, groups, win_type = standard_mahjong.can_win(hand)
        assert can_win is True

    def test_zero_as_normal_tile_in_eight_pairs(self, standard_mahjong):
        """测试八小对中0是普通牌"""
        hand_str = "0 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7"
        hand = parse_hand(hand_str)
        can_win, groups, win_type = standard_mahjong.can_win(hand)
        assert can_win is True

    def test_zero_as_joker_in_traditional(self, standard_mahjong):
        """测试传统麻将中0是万用牌"""
        hand_str = "1 2 3 4 5 6 7 7 7 8 8 8 11 11 12 0"
        hand = parse_hand(hand_str)
        can_win, groups, win_type = standard_mahjong.can_win(hand)
        assert can_win is True


# ============================================================
# 听牌测试 (TestReadyHand)
# ============================================================

class TestReadyHand:
    """测试听牌（テンパイ）判定"""

    def test_arithmetic_15_tile_ready(self, standard_mahjong):
        """测试15张牌的算术麻将听牌"""
        hand_str = "1 + 9 10 2 x 3 6 5 5 5 5 ^ ^ ^"
        hand = parse_hand(hand_str)
        is_ready, ready_info = standard_mahjong.is_ready(hand)
        assert is_ready is True
        assert "算术麻将" in ready_info
        assert '∧' in ready_info["算术麻将"]

    def test_traditional_15_tile_ready(self, standard_mahjong):
        """测试15张牌的传统麻将听牌"""
        hand_str = "1 2 3 4 5 6 7 7 7 8 8 8 11 11 12"
        hand = parse_hand(hand_str)
        is_ready, ready_info = standard_mahjong.is_ready(hand)
        assert is_ready is True
        assert "传统麻将" in ready_info
        assert 12 in ready_info["传统麻将"]

    def test_eight_pairs_15_tile_ready(self, standard_mahjong):
        """测试15张牌的八小对听牌"""
        hand_str = "1 1 2 2 3 3 4 4 5 5 6 6 7 7 8"
        hand = parse_hand(hand_str)
        is_ready, ready_info = standard_mahjong.is_ready(hand)
        assert is_ready is True

    def test_11_tile_ready_arithmetic_only(self, standard_mahjong):
        """测试11张牌听牌（只能听算术麻将）"""
        hand_str = "1 + 9 10 2 x 3 6 5 5 5"
        hand = parse_hand(hand_str)
        is_ready, ready_info = standard_mahjong.is_ready(hand)
        assert is_ready is True
        assert "算术麻将" in ready_info


# ============================================================
# 规则模式测试 (TestRuleModes)
# ============================================================

class TestRuleModes:
    """测试不同规则模式"""

    def test_standard_rule_rejects_sum_lt_10(self, standard_mahjong):
        """标准规则：加法和<10不能胡"""
        # 1 + 2 = 3，和小于10
        hand_str = "1 + 2 3 2 * 3 6 5 5 5 5 ^ ^ ^ ^"
        hand = parse_hand(hand_str)
        can_win, groups, win_type = standard_mahjong.can_win(hand)
        assert can_win is False

    def test_newbie_rule_accepts_sum_lt_10(self, newbie_mahjong):
        """新手规则：加法和<10可以胡"""
        # 1 + 2 = 3，和小于10，但新手规则允许
        hand_str = "1 + 2 3 2 * 3 6 5 5 5 5 ^ ^ ^ ^"
        hand = parse_hand(hand_str)
        can_win, groups, win_type = newbie_mahjong.can_win(hand)
        assert can_win is True
        assert win_type == "算术麻将"
