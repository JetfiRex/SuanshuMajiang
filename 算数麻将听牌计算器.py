"""
算术麻将命令行UI
提供交互式界面来判定胡牌和听牌
"""

from mahjong_checker import ArithmeticMahjong
from parser import parse_hand, format_hand

def print_welcome():
    """打印欢迎信息"""
    print("=" * 60)
    print("欢迎使用算术麻将胡牌判定器".center(60))
    print("=" * 60)
    print()

def print_help():
    """打印帮助信息"""
    print("【输入格式说明】")
    print("-" * 60)
    print("数字：直接输入数字，用空格分隔")
    print("符号：")
    print("  - 加号：+")
    print("  - 乘号：*, x, X, ×")
    print("  - 次方：^, ∧")
    print("万用牌：")
    print("  - 条子万用：条, 索, jt, ws, wcs, s")
    print("  - 筒子万用：筒, 饼, jtong, wp, wcm, p")
    print("  - 万字万用：万, jw, wm, wcl, m")
    print("  - 符号万用：符号, 箭, js, wz, wcop, op")
    print()
    print("示例：1 + 9 10 2 * 3 6 5 5 5 5 ^ ^ ^ ^")
    print("      1 2 3 s p m 4 5 6 7 7 7 8 8 8 op")
    print("-" * 60)
    print()

def choose_rule():
    """选择规则"""
    print("【选择规则】")
    print("1. 标准规则（加法和必须 ≥ 10）")
    print("2. 新手规则（加法和可以 < 10）")
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
    """选择判定模式"""
    print()
    print("【选择判定模式】")
    print("1. 判定16张牌是否能胡")
    print("2. 判定15张牌是否听牌")
    print("3. 判定11张牌是否听牌")
    print("4. 判定7张牌是否听牌")
    print("5. 判定3张牌是否听牌")
    print()

    while True:
        choice = input("请选择模式 (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print("❌ 无效选择，请输入 1-5")

def check_win(mjong):
    """判定16张牌是否能胡"""
    print()
    print("【判定16张牌是否能胡】")
    print("请输入16张牌：")

    while True:
        hand_str = input("> ").strip()

        if not hand_str:
            print("❌ 输入不能为空")
            continue

        try:
            hand = parse_hand(hand_str)

            if len(hand) != 16:
                print(f"❌ 输入了 {len(hand)} 张牌，需要16张牌")
                print("请重新输入：")
                continue

            # 判定胡牌
            can_win, groups, win_type = mjong.can_win(hand)

            print()
            print("=" * 60)
            print(f"手牌：{format_hand(hand)}")
            print("-" * 60)

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
            else:
                print("❌ 无法胡牌")

            print("=" * 60)
            break

        except ValueError as e:
            print(f"❌ 解析错误: {e}")
            print("请重新输入：")
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            print("请重新输入：")

def check_ready(mjong, num_tiles):
    """判定听牌"""
    tile_names = {
        15: "15张牌（可听算术麻将、传统麻将、八小对）",
        11: "11张牌（只能听算术麻将）",
        7: "7张牌（只能听算术麻将）",
        3: "3张牌（只能听算术麻将）"
    }

    print()
    print(f"【判定{tile_names[num_tiles]}是否听牌】")
    print(f"请输入{num_tiles}张牌：")

    while True:
        hand_str = input("> ").strip()

        if not hand_str:
            print("❌ 输入不能为空")
            continue

        try:
            hand = parse_hand(hand_str)

            if len(hand) != num_tiles:
                print(f"❌ 输入了 {len(hand)} 张牌，需要{num_tiles}张牌")
                print("请重新输入：")
                continue

            # 判定听牌
            is_ready, ready_info = mjong.is_ready(hand)

            print()
            print("=" * 60)
            print(f"手牌：{format_hand(hand)}")
            print("-" * 60)

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

                # 询问是否查看具体听牌后的胡牌形态
                print("-" * 60)
                choice = input("是否查看某张听牌能组成的具体胡牌形态？(y/n) [默认n]: ").strip().lower()

                if choice in ['y', 'yes']:
                    check_ready_detail(mjong, hand, ready_info)
            else:
                print("❌ 未听牌")

            print("=" * 60)
            break

        except ValueError as e:
            print(f"❌ 解析错误: {e}")
            print("请重新输入：")
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            print("请重新输入：")

def check_ready_detail(mjong, hand, ready_info):
    """查看具体听牌能组成的胡牌形态"""
    print()
    print("请输入想查看的听牌（输入牌面或序号，输入'all'查看所有）：")

    # 创建所有听牌的列表
    all_ready_tiles = []
    for win_type, tiles in ready_info.items():
        for tile in tiles:
            all_ready_tiles.append((tile, win_type))

    # 显示选项
    for i, (tile, win_type) in enumerate(all_ready_tiles, 1):
        print(f"  {i}. {tile} ({win_type})")

    while True:
        choice = input("> ").strip()

        if not choice:
            print("已取消")
            return

        # 检查是否查看所有
        if choice.lower() in ['all', '所有', 'a']:
            print()
            for idx, (tile, win_type) in enumerate(all_ready_tiles):
                show_ready_detail(mjong, hand, tile, win_type, idx + 1, len(all_ready_tiles))
                if idx < len(all_ready_tiles) - 1:
                    print()
            break

        # 尝试解析为序号
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(all_ready_tiles):
                target_tile, win_type = all_ready_tiles[idx]
            else:
                print(f"❌ 序号超出范围，请输入 1-{len(all_ready_tiles)}")
                continue
        except ValueError:
            # 尝试解析为牌面
            try:
                parsed = parse_hand(choice)
                if len(parsed) != 1:
                    print("❌ 请只输入一张牌")
                    continue
                target_tile = parsed[0]

                # 查找这张牌属于哪个胡法
                win_type = None
                for wt, tiles in ready_info.items():
                    if target_tile in tiles or str(target_tile) in [str(t) for t in tiles]:
                        win_type = wt
                        break

                if win_type is None:
                    print(f"❌ {target_tile} 不在听牌列表中")
                    continue

            except Exception as e:
                print(f"❌ 无法识别输入: {e}")
                continue

        show_ready_detail(mjong, hand, target_tile, win_type)

        # 询问是否继续查看其他听牌
        another = input("\n是否查看其他听牌形态？(y/n) [默认n]: ").strip().lower()
        if another not in ['y', 'yes']:
            break
        print()

def show_ready_detail(mjong, hand, target_tile, win_type, current=None, total=None):
    """显示单个听牌的详细信息"""
    # 组成完整手牌并判定
    test_hand = hand + [target_tile]

    header = "=" * 60
    if current is not None and total is not None:
        header = f"{'=' * 20} [{current}/{total}] {'=' * 20}"

    print(header)
    print(f"加入 {target_tile} 后的手牌：{format_hand(test_hand)}")
    print("-" * 60)

    can_win, groups, actual_win_type = mjong.can_win(test_hand)

    if can_win:
        print(f"✅ 可以胡牌！【{actual_win_type}】")
        print()
        if actual_win_type == "算术麻将":
            print("胡牌分组：")
            for i, group in enumerate(groups, 1):
                group_str = ' '.join(str(x) for x in group)
                if mjong.is_kezi(group):
                    print(f"  第{i}组（刻子）: {group_str}")
                else:
                    print(f"  第{i}组（算式）: {group_str}")
        elif actual_win_type == "传统麻将":
            print("胡牌组合：")
            for item in groups:
                if item[0] == '将':
                    print(f"  将牌: {item[1]} {item[2]}")
                elif item[0] == '刻子':
                    print(f"  刻子: {item[1]} {item[2]} {item[3]}")
                elif item[0] == '顺子':
                    print(f"  顺子: {item[1]} {item[2]} {item[3]}")
        elif actual_win_type == "八小对":
            print("对子组合：")
            for i, pair in enumerate(groups, 1):
                print(f"  第{i}对: {pair}")
    else:
        print("❌ 无法胡牌（可能存在bug）")

    print("=" * 60)

def main():
    """主函数"""
    print_welcome()
    print_help()

    # 选择规则
    mjong = choose_rule()
    print()
    print(f"已选择：{'标准规则' if mjong.require_sum_gte_10 else '新手规则'}")

    # 循环进行判定
    while True:
        mode = choose_mode()

        if mode == '1':
            check_win(mjong)
        elif mode == '2':
            check_ready(mjong, 15)
        elif mode == '3':
            check_ready(mjong, 11)
        elif mode == '4':
            check_ready(mjong, 7)
        elif mode == '5':
            check_ready(mjong, 3)

        # 询问是否继续
        print()
        choice = input("是否继续判定？(y/n) [默认y]: ").strip().lower()
        if choice == 'n' or choice == 'no':
            break

        print()

    # 退出提示
    print()
    print("=" * 60)
    print("感谢使用算术麻将胡牌判定器！".center(60))
    print("=" * 60)
    input("\n按任意键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已被用户中断")
        input("\n按任意键退出...")
    except Exception as e:
        print(f"\n程序发生错误: {e}")
        input("\n按任意键退出...")