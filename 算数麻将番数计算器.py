"""
算术麻将命令行UI（支持四种输入模式）
提供交互式界面来判定胡牌和听牌，并显示番数
"""

from calculator_base.mahjong_checker import ArithmeticMahjong
from calculator_base.parser import (
    parse_hand, format_hand,
    parse_mode1_already_won, 
    parse_mode2_check_win,
    parse_mode3_ready_with_meld,
    parse_mode4_ready_no_meld
)
from fan_calculator import calculate_fan

def print_welcome():
    """打印欢迎信息"""
    print("=" * 70)
    print("欢迎使用算术麻将胡牌判定器 (支持四种输入模式)".center(70))
    print("=" * 70)
    print()

def print_help():
    """打印帮助信息"""
    print("【四种输入模式说明】")
    print("-" * 70)
    print()
    print("模式1️: 16张已胡番数模式（最复杂，支持所有标记）")
    print("  格式: (鸣牌) (鸣牌) 手牌算式1 / 手牌算式2 [胡牌] {胡牌方式}")
    print("  示例: (11d) (2 2 2 2w) 3 + 10 13d / 5 + 7 12w / 9 [+] 5 14 {z}")
    print("  用途: 计算已胡牌的番数")
    print()
    print("模式2️: 16张是否胡模式")
    print("  格式: 16张牌（不分组，可以有括号鸣牌）")
    print("  示例: (1 + 9 10) 2 × 3 6 4 4 4 4 5 5 5 5")
    print("  用途: 判断是否能胡，如果能胡则显示分组和番数")
    print()
    print("模式3️: 有鸣牌听牌模式（15张）")
    print("  格式: (鸣牌) (鸣牌) 剩余牌（11/7/3张）")
    print("  示例: (1 + 9 10) (2 × 3 6) 4 4 4 5 5 5 5")
    print("  用途: 判断听什么牌（有鸣牌情况）")
    print()
    print("模式4️: 无鸣牌听牌模式（15张）")
    print("  格式: 15张牌（无鸣牌，无括号）")
    print("  示例: 1 + 9 2 × 3 6 4 4 4 4 5 5 5 5")
    print("  用途: 判断听什么牌（无鸣牌情况）")
    print()
    print("【标记说明】")
    print("  (牌) - 鸣牌（吃/碰/杠）")
    print("  / 或 | - 手牌分组分隔符")
    print("  [牌] - 胡牌标记")
    print("  {方式} - 胡牌方式（z=自摸, k=杠上开花, h=海底捞月, q=抢杠, t=天胡）")
    print("  d后缀 - 宝牌（dora）")
    print("  w后缀 - 万用牌替换")
    print()
    print("【数字和符号】")
    print("  数字: 0-19, 20-49（需万用）")
    print("  符号: +（加）, *或×（乘）, ^或∧（次方）")
    print("  万用: 条/s, 筒/p, 万/m, 符号/op")
    print("-" * 70)
    print()

def choose_rule():
    """选择规则"""
    print("【选择规则】")
    print("1. 进阶规则（加法和必须 ≥ 10，起胡8番）")
    print("2. 新手规则（加法和可以 < 10，起胡0番）")
    print()

    while True:
        choice = input("请选择规则 (1/2) [默认1]: ").strip()
        if choice == '' or choice == '1':
            return ArithmeticMahjong(require_sum_gte_10=True)
        elif choice == '2':
            return ArithmeticMahjong(require_sum_gte_10=False)
        else:
            print("❌ 无效选择，请输入 1 或 2")

def choose_mode():
    """选择输入模式"""
    print()
    print("【选择输入模式】")
    print("1️. 模式1: 16张已胡番数模式（已分组，有鸣牌标记）")
    print("2️. 模式2: 16张是否胡模式（未分组）")
    print("3️. 模式3: 有鸣牌听牌模式（15/11/7/3张）")
    print("4️. 模式4: 无鸣牌听牌模式（15/11/7/3张）")
    print()

    while True:
        choice = input("请选择模式 (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        else:
            print("❌ 无效选择，请输入 1-4")

def mode1_already_won(mjong):
    """模式1：16张已胡番数模式"""
    print()
    print("=" * 70)
    print("模式1️: 16张已胡番数模式")
    print("=" * 70)
    print("格式: (鸣牌) 手牌分组 / 手牌分组 [胡牌] {胡牌方式}")
    print("示例: (11d) (2 2 2 2w) 3 + 10 13d / 5 + 7 12w / 9 [+] 5 14 {z}")
    print()

    while True:
        hand_str = input("请输入手牌 (直接回车返回): ").strip()

        if not hand_str:
            print("已取消")
            return

        try:
            # 解析模式1
            hand = parse_mode1_already_won(hand_str)
            
            print()
            print("=" * 70)
            print(f"解析结果:")
            print("-" * 70)
            
            # 显示鸣牌
            if hand.melded_groups:
                print("鸣牌:")
                for i, mg in enumerate(hand.melded_groups, 1):
                    tiles_str = ' '.join(str(t.value) for t in mg.tiles)
                    print(f"  {i}. {mg.group_type}: {tiles_str}")
            
            # 显示手牌分组
            if hand.hand_groups:
                print("手牌分组:")
                for i, group in enumerate(hand.hand_groups, 1):
                    tiles_str = ' '.join(str(t.value) for t in group)
                    print(f"  第{i}组: {tiles_str}")
            
            # 显示胡牌和胡牌方式
            if hand.winning_tile:
                print(f"胡牌: {hand.winning_tile.value}")
            if hand.winning_method:
                print(f"胡牌方式: {hand.winning_method}")
            
            print("-" * 70)
            
            # 计算番数
            result = calculate_fan(hand, min_fan=mjong.min_fan)
            
            print()
            print(f"📊 总番数: {result.get_total_fan()}番")
            
            if result.get_total_fan() >= mjong.min_fan:
                print(f"✅ 满足起胡条件（{mjong.min_fan}番起胡）")
            else:
                print(f"❌ 不满足起胡条件（需要{mjong.min_fan}番，当前{result.get_total_fan()}番）")
            
            if result.results:
                print()
                print("番种明细：")
                for fan in result.results:
                    print(f"  • {fan}")
            
            print("=" * 70)
            break

        except ValueError as e:
            print(f"❌ 解析错误: {e}")
            print("请重新输入：")
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()
            print("请重新输入：")

def mode2_win_check(mjong):
    """模式2：16张是否胡模式"""
    print()
    print("=" * 70)
    print("模式2️: 16张是否胡模式")
    print("=" * 70)
    print("格式: 16张牌（可以有鸣牌括号）")
    print("示例: (1 + 9 10) 2 × 3 6 4 4 4 4 5 5 5 5")
    print()

    while True:
        hand_str = input("请输入16张牌 (直接回车返回): ").strip()

        if not hand_str:
            print("已取消")
            return

        try:
            # 解析模式2
            hand = parse_mode2_check_win(hand_str)
            
            # 提取所有牌
            tiles = []
            has_melded = False
            
            # 检查是否有鸣牌
            if hasattr(hand, 'melded_groups') and hand.melded_groups:
                has_melded = True
                for mg in hand.melded_groups:
                    tiles.extend([t.value for t in mg.tiles])
            
            # 添加手牌
            if hasattr(hand, 'hand_tiles'):
                tiles.extend([t.value for t in hand.hand_tiles])
            elif hasattr(hand, 'tiles'):
                tiles.extend([t.value for t in hand.tiles])
            
            # 使用mahjong_checker判断是否能胡
            can_win, groups, win_type, fan_info = mjong.can_win(tiles, has_melded=has_melded)
            
            print()
            print("=" * 70)
            
            if can_win:
                print(f"✅ 可以胡牌！【{win_type}】")
                print()
                
                if win_type == "算术麻将":
                    print("胡牌分组：")
                    for i, group in enumerate(groups, 1):
                        group_str = ' '.join(str(x) for x in group)
                        if mjong.is_kezi(group):
                            print(f"  第{i}组（刻子）: {group_str}")
                        else:
                            print(f"  第{i}组（算式）: {group_str}")
                else:
                    print(f"胡牌组合：{groups}")
                
                # 显示番数信息
                if fan_info:
                    print()
                    print("-" * 70)
                    print(f"📊 总番数: {fan_info['total_fan']}番")
                    
                    if fan_info['can_start']:
                        print(f"✅ 满足起胡条件（{mjong.min_fan}番起胡）")
                    else:
                        print(f"❌ 不满足起胡条件（需要{mjong.min_fan}番，当前{fan_info['total_fan']}番）")
                    
                    if fan_info.get('fan_result'):
                        print()
                        print("番种明细：")
                        for fan in fan_info['fan_result'].results:
                            print(f"  • {fan}")
            else:
                print("❌ 无法胡牌")
            
            print("=" * 70)
            break

        except ValueError as e:
            print(f"❌ 解析错误: {e}")
            print("请重新输入：")
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()
            print("请重新输入：")

def mode3_ready_with_melded(mjong):
    """模式3：有鸣牌听牌模式"""
    print()
    print("=" * 70)
    print("模式3️: 有鸣牌听牌模式")
    print("=" * 70)
    print("格式: (鸣牌) (鸣牌) 剩余牌")
    print("示例: (1 + 9 10) (2 × 3 6) 4 4 4 5 5 5 5  (15张)")
    print("      (1 + 9 10) (2 × 3 6) (3 3 3 3) 4 4 4  (11张)")
    print()

    while True:
        hand_str = input("请输入手牌 (直接回车返回): ").strip()

        if not hand_str:
            print("已取消")
            return

        try:
            # 解析模式3
            hand = parse_mode3_ready_with_meld(hand_str)
            
            # 合并所有牌用于听牌判断
            all_tiles = []
            for mg in hand.melded_groups:
                all_tiles.extend([t.value for t in mg.tiles])
            if hand.hand_tiles:
                all_tiles.extend([t.value for t in hand.hand_tiles])
            
            # 判断听牌
            is_ready, ready_info = mjong.is_ready(all_tiles)
            
            print()
            print("=" * 70)
            print(f"手牌: {' '.join(str(t) for t in all_tiles)} ({len(all_tiles)}张)")
            print("-" * 70)

            if is_ready:
                print("✅ 听牌！")
                print()
                for win_type, tiles in ready_info.items():
                    print(f"【{win_type}】听：")
                    # 每行最多显示10个牌
                    tiles_str = [str(t) for t in tiles]
                    for i in range(0, len(tiles_str), 10):
                        chunk = tiles_str[i:i+10]
                        print(f"  {', '.join(chunk)}")
                    print()
            else:
                print("❌ 未听牌")

            print("=" * 70)
            break

        except ValueError as e:
            print(f"❌ 解析错误: {e}")
            print("请重新输入：")
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()
            print("请重新输入：")

def mode4_ready_no_melded(mjong):
    """模式4：无鸣牌听牌模式"""
    print()
    print("=" * 70)
    print("模式4️: 无鸣牌听牌模式")
    print("=" * 70)
    print("格式: 15/11/7/3张牌（无鸣牌）")
    print("示例: 1 + 9 2 × 3 6 4 4 4 4 5 5 5 5  (15张)")
    print("      1 + 9 2 × 3 6 4 4 4 5 5 5  (11张)")
    print()

    while True:
        hand_str = input("请输入手牌 (直接回车返回): ").strip()

        if not hand_str:
            print("已取消")
            return

        try:
            # 解析模式4
            hand = parse_mode4_ready_no_meld(hand_str)
            
            # 获取所有牌
            all_tiles = [t.value for t in hand.hand_tiles]
            
            # 判断听牌
            is_ready, ready_info = mjong.is_ready(all_tiles)
            
            print()
            print("=" * 70)
            print(f"手牌: {' '.join(str(t) for t in all_tiles)} ({len(all_tiles)}张)")
            print("-" * 70)

            if is_ready:
                print("✅ 听牌！")
                print()
                for win_type, tiles in ready_info.items():
                    print(f"【{win_type}】听：")
                    # 每行最多显示10个牌
                    tiles_str = [str(t) for t in tiles]
                    for i in range(0, len(tiles_str), 10):
                        chunk = tiles_str[i:i+10]
                        print(f"  {', '.join(chunk)}")
                    print()
            else:
                print("❌ 未听牌")

            print("=" * 70)
            break

        except ValueError as e:
            print(f"❌ 解析错误: {e}")
            print("请重新输入：")
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()
            print("请重新输入：")

def main():
    """主函数"""
    print_welcome()
    print_help()

    # 选择规则
    mjong = choose_rule()
    print()
    print(f"已选择：{'进阶规则（加法≥10，起胡8番）' if mjong.require_sum_gte_10 else '新手规则（加法可<10，起胡0番）'}")

    # 循环进行判定
    while True:
        mode = choose_mode()

        if mode == '1':
            mode1_already_won(mjong)
        elif mode == '2':
            mode2_win_check(mjong)
        elif mode == '3':
            mode3_ready_with_melded(mjong)
        elif mode == '4':
            mode4_ready_no_melded(mjong)

        # 询问是否继续
        print()
        choice = input("是否继续判定？(y/n) [默认n]: ").strip().lower()
        if choice == 'y' or choice == 'yes':
            pass
        else:
            break

        print()

    # 退出提示
    print()
    print("=" * 70)
    print("感谢使用算术麻将胡牌判定器！".center(70))
    print("=" * 70)
    input("\n按任意键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已被用户中断")
        input("\n按任意键退出...")
    except Exception as e:
        print(f"\n程序发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按任意键退出...")

