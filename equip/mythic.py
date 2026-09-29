"""装备神话与超越系统 - 含10个bug"""
from dataclasses import dataclass, field

@dataclass
class Equipment:
    eid: str
    name: str
    level: int = 1
    quality: str = "common"
    slot: str = "weapon"
    is_mythic: bool = False  # bug1: 无条件
    mythic_stage: int = 0  # bug3: 无阶段限制
    mythic_skill: str = ""  # bug2: 固定技能
    mythic_id: str = ""

class MythicSystem:
    def __init__(self):
        self.equipment: dict[str, Equipment] = {}
        self.mythic_tasks: dict = {}  # bug10: 无任务

    def can_awaken_mythic(self, eid: str) -> bool:
        # bug1: 无条件
        return True

    def get_mythic_skill(self, mythic_type: str) -> str:
        # bug2: 固定技能
        return "mythic_power"

    def can_breakthrough_stage(self, current_stage: int, target_stage: int) -> bool:
        # bug3: 跳阶
        return True

    def check_mythic_set(self, items: list) -> dict:
        # bug4: 不看ID只看数量
        if len(items) >= 3:
            return {"bonus": "3piece"}
        return {}

    def get_mythic_legacy_rate(self) -> float:
        # bug5: 全继承
        return 1.0

    def is_mythic_illusion_unlocked(self, illusion_id: str) -> bool:
        # bug6: 默认开放
        return True

    def can_awaken_mythic_slot(self, from_slot: str, to_slot: str) -> bool:
        # bug7: 跨部位
        return True

    def get_mythic_breakthrough_rate(self, stage: int) -> float:
        # bug8: 100%成功
        return 1.0

    def get_resonance_by_stage(self, stage: int) -> float:
        # bug9: 不看阶数
        return 1.0

    def needs_mythic_quest(self, eid: str) -> bool:
        # bug10: 无任务
        return False
