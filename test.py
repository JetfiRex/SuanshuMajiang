"""
算术麻将胡牌判定器测试示例
展示如何使用 ArithmeticMahjong 类
"""

from ArithmeticMahjong import ArithmeticMahjong, parse_hand, format_hand


def main():
    print("=" * 60)
    print("算术麻将胡牌判定器测试")
    print("=" * 60)

    # 演示解析器使用
    print("\n【解析器示例】")
    print("-" * 60)

    # 示例1：使用不同的乘号表示
    hand_str1 = "1 + 9 10 2 * 3 6 5 5 5 5 ^ ^ ^ ^"
    print(f"输入字符串: {hand_str1}")
    hand1 = parse_hand(hand_str1)
    print(f"解析结果: {hand1}")
    print(f"格式化输出: {format_hand(hand1)}")

    # 示例2：使用逗号分隔
    hand_str2 = "1,+,9,10,2,x,3,6,5,5,5,5,^,^,^,^"
    print(f"\n输入字符串: {hand_str2}")
    hand2 = parse_hand(hand_str2)
    print(f"解析结果: {hand2}")

    # 示例3：使用X表示乘号
    hand_str3 = "2 X 3 6"
    print(f"\n输入字符串: {hand_str3}")
    hand3 = parse_hand(hand_str3)
    print(f"解析结果: {hand3}")

    print("\n" + "=" * 60)

    # 创建标准规则的判定器
    print("\n【标准规则】加法和必须>=10")
    mjong_standard = ArithmeticMahjong(require_sum_gte_10=True)

    # 测试1: 算术麻将胡牌
    print("\n【测试1】算术麻将胡牌（16张）")
    hand_str = "1 + 9 10 2 * 3 6 5 5 5 5 ^ ^ ^ ^"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)

    can_win, groups, win_type = mjong_standard.can_win(hand)
    print(mjong_standard.format_result(can_win, groups, win_type))

    # 测试2: 算术麻将听牌
    print("\n【测试2】算术麻将听牌（15张）")
    hand_str = "1 + 9 10 2 x 3 6 5 5 5 5 ^ ^ ^"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)

    is_ready, ready_info = mjong_standard.is_ready(hand)
    print(f"手牌（15张）: {format_hand(hand)}")
    if is_ready:
        print("听牌！")
        for win_type, tiles in ready_info.items():
            print(f"  【{win_type}】听: {tiles}")
    else:
        print("未听牌")

    # 测试3: 传统麻将胡牌
    print("\n【测试3】传统麻将胡牌（16张）")
    hand_str = "1 2 3 4 5 6 7 7 7 8 8 8 11 11 12 12"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)

    can_win, groups, win_type = mjong_standard.can_win(hand)
    print(mjong_standard.format_result(can_win, groups, win_type))

    # 测试4: 传统麻将听牌
    print("\n【测试4】传统麻将听牌（15张）")
    hand_str = "1 2 3 4 5 6 7 7 7 8 8 8 11 11 12"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)

    is_ready, ready_info = mjong_standard.is_ready(hand)
    print(f"手牌（15张）: {format_hand(hand)}")
    if is_ready:
        print("听牌！")
        for win_type, tiles in ready_info.items():
            print(f"  【{win_type}】听: {tiles}")
    else:
        print("未听牌")

    # 测试5: 八小对胡牌
    print("\n【测试5】八小对胡牌（16张）")
    hand_str = "1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)

    can_win, groups, win_type = mjong_standard.can_win(hand)
    print(mjong_standard.format_result(can_win, groups, win_type))

    # 测试6: 八小对听牌
    print("\n【测试6】八小对听牌（15张）")
    hand_str = "1 1 2 2 3 3 4 4 5 5 6 6 7 7 8"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)

    is_ready, ready_info = mjong_standard.is_ready(hand)
    print(f"手牌（15张）: {format_hand(hand)}")
    if is_ready:
        print("听牌！")
        for win_type, tiles in ready_info.items():
            print(f"  【{win_type}】听: {tiles}")
    else:
        print("未听牌")

    # 测试7: 11张牌听牌（只能听算术麻将）
    print("\n【测试7】11张牌听牌（只能听算术麻将）")
    hand_str = "1 + 9 10 2 x 3 6 5 5 5"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)

    is_ready, ready_info = mjong_standard.is_ready(hand)
    print(f"手牌（11张）: {format_hand(hand)}")
    if is_ready:
        print("听牌！")
        for win_type, tiles in ready_info.items():
            print(f"  【{win_type}】听: {tiles}")
    else:
        print("未听牌")

    # 测试8: 带万用牌的算术麻将（使用简写）
    print("\n【测试8】带万用牌的算术麻将（16张，使用简写）")
    hand_str = "1 + 9 10 2 x 3 6 5 5 5 5 条 ^ ^"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)
    print(f"解析后: {hand}")

    can_win, groups, win_type = mjong_standard.can_win(hand)
    print(mjong_standard.format_result(can_win, groups, win_type))

    # 测试9: 带万用牌的传统麻将（使用简写）
    print("\n【测试9】带万用牌的传统麻将（16张，使用简写）")
    hand_str = "1 2 3 4 5 6 7 7 7 8 8 8 11 11 12 筒"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)
    print(f"解析后: {hand}")

    can_win, groups, win_type = mjong_standard.can_win(hand)
    print(mjong_standard.format_result(can_win, groups, win_type))

    # 测试10: 八小对中0是普通牌
    print("\n【测试10】八小对中0是普通牌（16张）")
    hand_str = "0 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)

    can_win, groups, win_type = mjong_standard.can_win(hand)
    print(mjong_standard.format_result(can_win, groups, win_type))

    # 测试11: 传统麻将中0是万用牌
    print("\n【测试11】传统麻将中0是万用牌（16张）")
    hand_str = "1 2 3 4 5 6 7 7 7 8 8 8 11 11 12 0"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)

    can_win, groups, win_type = mjong_standard.can_win(hand)
    print(mjong_standard.format_result(can_win, groups, win_type))

    # 测试12: 万用牌的多种简写
    print("\n【测试12】万用牌的多种简写方式")
    test_inputs = [
        "条 筒 万 符号",
        "索 饼 万字万用 箭",
        "jt jtong jw js"
    ]
    for test_str in test_inputs:
        print(f"  输入: '{test_str}' -> {parse_hand(test_str)}")

    # 测试13: 新手规则（加法和可以<10）
    print("\n" + "=" * 60)
    print("\n【新手规则】加法和可以<10")
    mjong_newbie = ArithmeticMahjong(require_sum_gte_10=False)

    hand_str = "1 + 2 3 2 * 3 6 5 5 5 5 ^ ^ ^ ^"
    print(f"输入: {hand_str}")
    hand = parse_hand(hand_str)

    can_win, groups, win_type = mjong_newbie.can_win(hand)
    print(mjong_newbie.format_result(can_win, groups, win_type))

    print("\n同样的牌在标准规则下：")
    can_win_std, groups_std, win_type_std = mjong_standard.can_win(hand)
    print(mjong_standard.format_result(can_win_std, groups_std, win_type_std))


if __name__ == "__main__":
    main()