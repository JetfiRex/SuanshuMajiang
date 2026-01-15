"""
算术麻将番数计算 - 基础模块
定义番种枚举、牌库信息、工具函数等
"""

from enum import Enum
from typing import List, Set, Dict, Tuple
from hand_structure import Hand, Tile, MeldedGroup
from parser import PLUS, MULTIPLY, POWER, SYMBOLS


class FanType(Enum):
    """番种枚举"""
    # 88番
    DA_SAN_YUAN = (88, "大三元")
    DA_SI_XI = (88, "大四喜")
    QI_YI_SE = (88, "奇一色")
    TIAN_LONG = (88, "天龙")
    LIAN_BA_DUI = (88, "连八对")
    WU_HE_SHU = (88, "无合数")
    SHI_SAN_YAO = (88, "十三幺")
    SI_TONG_SHI = (88, "四同式")
    SI_KE_ZI = (88, "四刻子")
    BA_XIAN_GUO_HAI = (88, "八仙过海")
    
    # 64番
    QUAN_ER_MI = (64, "全二幂")
    CI_YI_SE = (64, "次一色")
    LIANG_BAN_GAO = (64, "两般高")
    
    # 48番
    QUAN_ER_WEI = (48, "全二位")
    SAN_KE_ZI = (48, "三刻子")
    SAN_TONG_SHI = (48, "三同式")
    QUAN_DUO_BEI = (48, "全多倍")
    QUAN_CAI = (48, "全彩")
    
    # 32番
    XIAO_SAN_YUAN = (32, "小三元")
    DI_LONG = (32, "地龙")
    XIAO_SI_XI = (32, "小四喜")
    TIAN_HU = (32, "天胡")
    
    # 24番
    SI_XIAN_GUO_HAI = (24, "四仙过海")
    BA_XIAO_DUI = (24, "八小对")
    QUAN_YI_WEI = (24, "全一位")
    QUAN_SAN_BEI = (24, "全三倍")
    
    # 16番
    QUAN_HE_SHU = (16, "全合数")
    QUAN_OU_SHU = (16, "全偶数")
    HAI_DI_LAO_YUE = (16, "海底捞月")
    
    # 12番
    JIA_YI_SE = (12, "加一色")
    SI_MEN_QI = (12, "四门齐")
    CHENG_YI_SE = (12, "乘一色")
    
    # 8番
    YI_BAN_GAO = (8, "一般高")
    QUAN_DAI_CAI = (8, "全带彩")
    CHUAN_TONG_MAJIANG = (8, "传统麻将")
    WU_FAN_HU = (8, "无番胡")
    GANG_SHANG_KAI_HUA = (8, "杠上开花")
    QIANG_GANG = (8, "抢杠")
    
    # 6番
    DUAN_ER = (6, "断二")
    BU_QIU_REN = (6, "不求人")
    
    # 4番
    PING_HU = (4, "平胡")
    YANG_YANG = (4, "鸳鸯")
    QUAN_QIU_REN = (4, "全求人")
    AN_KE = (4, "暗刻")
    GANG = (4, "杠")
    
    # 2番
    TING_FU_HAO = (2, "听符号")
    MEN_QING = (2, "门清")
    MING_KE = (2, "明刻")
    BAO_PAI = (2, "宝牌")
    CI_FANG = (2, "次方")
    
    def __init__(self, fan_value: int, name: str):
        self.fan_value = fan_value
        self.fan_name = name


# 牌面张数映射（用于平胡、鸳鸯等判断）
TILE_COUNTS = {
    # 数字牌
    0: 2,
    1: 2,
    2: 10,
    3: 8,
    4: 6,
    5: 6,
    6: 6,
    7: 4,  # 普通7
    8: 6,
    9: 4,
    10: 4,
    11: 2,  # 1张普通 + 1张dora
    12: 6,
    13: 2,  # 1张普通 + 1张dora
    14: 2,
    15: 2,
    16: 4,
    17: 2,  # 1张普通 + 1张dora
    18: 4,
    19: 2,  # 1张普通 + 1张dora
    20: 2,
    21: 2,
    24: 4,
    25: 2,
    27: 2,
    28: 2,
    30: 2,
    32: 2,
    35: 2,
    36: 2,
    40: 2,
    49: 2,
    # 符号
    PLUS: 10,
    MULTIPLY: 12,
    POWER: 6,
}


class FanResult:
    """单个番种的判定结果"""
    
    def __init__(self, fan_type: FanType, count: int = 1, reason: str = ""):
        """
        初始化番种结果
        
        参数：
            fan_type: 番种类型
            count: 数量（如宝牌可能有多张）
            reason: 说明（可选）
        """
        self.fan_type = fan_type
        self.count = count
        self.reason = reason
    
    def get_total_fan(self) -> int:
        """获取总番数"""
        return self.fan_type.fan_value * self.count
    
    def __repr__(self):
        """字符串表示"""
        if self.count > 1:
            return f"{self.fan_type.fan_name} x{self.count} ({self.get_total_fan()}番)"
        else:
            return f"{self.fan_type.fan_name} ({self.get_total_fan()}番)"


class FanResults:
    """番数计算的完整结果"""
    
    def __init__(self):
        self.results: List[FanResult] = []
        self.excluded: List[Tuple[FanType, str]] = []  # 被排除的番种及原因
    
    def add(self, fan_result: FanResult):
        """添加一个番种结果"""
        self.results.append(fan_result)
    
    def exclude(self, fan_type: FanType, reason: str):
        """记录一个被排除的番种"""
        self.excluded.append((fan_type, reason))
    
    def get_total_fan(self) -> int:
        """获取总番数"""
        return sum(r.get_total_fan() for r in self.results)
    
    def get_starting_fan(self, hand=None) -> int:
        """
        获取起胡番数（用于判断是否满足起胡条件）
        
        规则：
        - 单张杠的宝牌不算起胡番，但算总番
        - 单张杠的万用牌算起胡番
        
        参数：
            hand: Hand对象（用于判断单张杠宝牌）
        
        返回：
            起胡番数
        """
        total = 0
        
        # 统计单张杠宝牌数量
        dora_single_gang_count = 0
        if hand and hasattr(hand, 'melded_groups'):
            for melded in hand.melded_groups:
                if melded.group_type == 'single_gang':
                    tile = melded.tiles[0]
                    tile_str = str(tile)
                    dora_tiles = ['11d', '13d', '17d', '19d']
                    if tile_str in dora_tiles or (hasattr(tile, 'is_dora') and tile.is_dora):
                        dora_single_gang_count += 1
        
        # 计算起胡番：排除单张杠宝牌的番数
        for result in self.results:
            if result.fan_type == FanType.BAO_PAI:
                # 宝牌番：只有单张杠的万用牌算起胡番
                joker_count = result.count - dora_single_gang_count
                if joker_count > 0:
                    total += result.fan_type.fan_value * joker_count
            else:
                # 其他番种都算起胡番
                total += result.get_total_fan()
        
        return total
    
    def has_fan_type(self, fan_type: FanType) -> bool:
        """检查是否包含某个番种"""
        return any(r.fan_type == fan_type for r in self.results)
    
    def sort_by_value(self):
        """按番值从大到小排序"""
        self.results.sort(key=lambda r: r.fan_type.fan_value, reverse=True)
    
    def __repr__(self):
        """字符串表示"""
        lines = [f"总计: {self.get_total_fan()}番"]
        lines.append("-" * 40)
        for result in self.results:
            lines.append(str(result))
        return "\n".join(lines)


# ============================================================
# 不重复规则 - 番种依赖关系
# ============================================================

# 格式: {高级番种: [被包含的低级番种列表]}
FAN_EXCLUSIONS = {
    # 88番排除规则
    FanType.DA_SAN_YUAN: [FanType.SAN_KE_ZI, FanType.XIAO_SAN_YUAN],
    FanType.SI_KE_ZI: [FanType.SAN_KE_ZI, FanType.AN_KE, FanType.MING_KE],
    FanType.QI_YI_SE: [FanType.DUAN_ER],
    FanType.SI_TONG_SHI: [FanType.SAN_TONG_SHI, FanType.LIANG_BAN_GAO, FanType.YI_BAN_GAO],
    FanType.LIAN_BA_DUI: [FanType.BA_XIAO_DUI, FanType.MEN_QING],  # 连八对包含八小对，且是门清
    FanType.TIAN_LONG: [FanType.DI_LONG, FanType.MEN_QING, FanType.QUAN_DAI_CAI, FanType.QUAN_CAI],  # 天龙包含地龙、门清、全带彩、全彩
    
    # 64番排除规则
    FanType.CI_YI_SE: [FanType.CI_FANG],
    FanType.LIANG_BAN_GAO: [FanType.YI_BAN_GAO],
    
    # 48番排除规则
    FanType.SAN_KE_ZI: [FanType.AN_KE, FanType.MING_KE],
    FanType.SAN_TONG_SHI: [FanType.LIANG_BAN_GAO, FanType.YI_BAN_GAO],
    FanType.QUAN_DUO_BEI: [FanType.QUAN_SAN_BEI],
    FanType.QUAN_CAI: [FanType.QUAN_DAI_CAI],  # 全彩包含全带彩
    
    # 32番排除规则
    FanType.XIAO_SAN_YUAN: [],
    FanType.DI_LONG: [FanType.MEN_QING, FanType.QUAN_DAI_CAI, FanType.QUAN_CAI],  # 地龙包含门清、全带彩、全彩
    
    # 12番排除规则
    FanType.JIA_YI_SE: [FanType.DUAN_ER],
    FanType.SI_MEN_QI: [FanType.MING_KE, FanType.AN_KE, FanType.CI_FANG],  # 不计刻子和次方本身
    FanType.CHENG_YI_SE: [],
    
    # 门清限定的番不叠加"门清"，但可以叠加"不求人"
    FanType.BU_QIU_REN: [FanType.MEN_QING],  # 不求人包含门清
    FanType.BA_XIAO_DUI: [FanType.MEN_QING],  # 八小对是门清
    FanType.CHUAN_TONG_MAJIANG: [FanType.MEN_QING],  # 传统麻将必然是门清
}


def apply_exclusion_rules(fan_results: FanResults) -> FanResults:
    """
    应用不重复规则，排除被包含的番种
    
    参数：
        fan_results: 原始番数结果
    
    返回：
        应用规则后的番数结果
    """
    # 创建新结果
    final_results = FanResults()
    
    # 获取所有已有的番种
    present_fan_types = {r.fan_type for r in fan_results.results}
    
    # 收集所有应该被排除的番种
    excluded_types = set()
    for result in fan_results.results:
        if result.fan_type in FAN_EXCLUSIONS:
            for excluded_type in FAN_EXCLUSIONS[result.fan_type]:
                if excluded_type in present_fan_types:
                    excluded_types.add(excluded_type)
                    final_results.exclude(
                        excluded_type,
                        f"被{result.fan_type.fan_name}包含"
                    )
    
    # 添加未被排除的番种
    for result in fan_results.results:
        if result.fan_type not in excluded_types:
            final_results.add(result)
        else:
            # 记录被排除的番种（如果还没记录）
            if not any(ft == result.fan_type for ft, _ in final_results.excluded):
                final_results.exclude(result.fan_type, "被其他番种包含")
    
    return final_results


# ============================================================
# 工具函数
# ============================================================

def get_tile_count(tile_value) -> int:
    """
    获取牌面张数
    
    参数：
        tile_value: 牌值（int或str）
    
    返回：
        牌面张数
    """
    return TILE_COUNTS.get(tile_value, 0)


def is_prime(n: int) -> bool:
    """判断是否是质数"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def is_composite(n: int) -> bool:
    """判断是否是合数"""
    return n > 1 and not is_prime(n)


def is_power_of_2(n: int) -> bool:
    """判断是否是2的幂"""
    return n > 0 and (n & (n - 1)) == 0


def get_all_number_tiles(hand: Hand) -> List[int]:
    """
    获取所有数字牌（包括鸣牌和万用牌替代的，但不包括单张杠）
    
    用于"全"字开头的番种判断（奇一色、全一位、无合数等）
    
    参数：
        hand: Hand对象
    
    返回：
        数字牌列表（万用牌显示替代后的值）
    """
    numbers = []
    
    # 从鸣牌中提取（不包括单张杠）
    for melded_group in hand.melded_groups:
        if melded_group.group_type != 'single_gang':
            for tile in melded_group.tiles:
                if isinstance(tile.value, int):
                    numbers.append(tile.value)
    
    # 从手牌分组中提取
    if hand.hand_groups:
        for group in hand.hand_groups:
            for tile in group:
                if isinstance(tile.value, int):
                    numbers.append(tile.value)
    # 从未分组手牌中提取
    elif hand.hand_tiles:
        for tile in hand.hand_tiles:
            if isinstance(tile.value, int):
                numbers.append(tile.value)
    
    return numbers


def get_all_tiles_for_fan(hand: Hand, include_single_gang: bool = False) -> List[Tile]:
    """
    获取用于番数计算的所有牌
    
    参数：
        hand: Hand对象
        include_single_gang: 是否包括单张杠的牌
    
    返回：
        牌列表
    """
    tiles = []
    
    # 鸣牌（根据规则决定是否包括单张杠）
    for group in hand.melded_groups:
        if group.group_type == 'single_gang':
            if include_single_gang:
                tiles.extend(group.tiles)
        else:
            tiles.extend(group.tiles)
    
    # 手牌
    if hand.hand_groups:
        for group in hand.hand_groups:
            tiles.extend(group)
    elif hand.hand_tiles:
        tiles.extend(hand.hand_tiles)
    
    return tiles
