"""装备神话与超越系统"""
from dataclasses import dataclass, field

MAX_EQUIP_LEVEL = 60
MAX_MYTHIC_STAGE = 10
AWAKEN_SHARDS_REQUIRED = 50
AWAKEN_STONES_REQUIRED = 10
SET_BONUS_THRESHOLD = 3
BASE_LEGACY_RATE = 0.5
LEGACY_STAGE_DECAY = 0.03
GUARANTEE_THRESHOLD = 5

MYTHIC_SKILLS = {
    "destruction": {"ultimate": "annihilation_strike", "passive": "wrath_of_ruin"},
    "protection": {"ultimate": "aegis_of_eternity", "passive": "guardian_bulwark"},
    "swiftness": {"ultimate": "tempest_dash", "passive": "wind_veil"},
    "wisdom": {"ultimate": "arcane_revelation", "passive": "sage_insight"},
    "vitality": {"ultimate": "phoenix_rebirth", "passive": "life_spring"},
}

MYTHIC_QUEST_CHAINS = {
    "destruction": ["mq_dest_1", "mq_dest_2", "mq_dest_3"],
    "protection": ["mq_prot_1", "mq_prot_2", "mq_prot_3"],
    "swiftness": ["mq_swift_1", "mq_swift_2", "mq_swift_3"],
    "wisdom": ["mq_wis_1", "mq_wis_2", "mq_wis_3"],
    "vitality": ["mq_vita_1", "mq_vita_2", "mq_vita_3"],
}

STAGE_MATERIALS = {
    stage: {"mythic_shards": 10 * stage, "awakening_stones": 2 * stage}
    for stage in range(1, MAX_MYTHIC_STAGE + 1)
}

STAGE_BREAKTHROUGH_RATES = {
    1: 0.95, 2: 0.90, 3: 0.85, 4: 0.75, 5: 0.65,
    6: 0.55, 7: 0.45, 8: 0.35, 9: 0.25, 10: 0.15,
}


@dataclass
class Equipment:
    eid: str
    name: str
    level: int = 1
    quality: str = "common"
    slot: str = "weapon"
    is_mythic: bool = False
    mythic_stage: int = 0
    mythic_skill: str = ""
    mythic_id: str = ""
    mythic_type: str = ""
    mythic_shards: int = 0
    awakening_stones: int = 0
    quest_completed: bool = False
    breakthrough_failures: int = 0


class MythicSystem:
    def __init__(self):
        self.equipment: dict[str, Equipment] = {}
        self.mythic_tasks: dict = {}
        self.completed_quests: set = set()
        self.unlocked_illusions: set = set()
        self.achievements: set = set()

    # bug1: 觉醒需要严格条件：传说满级 + 神话碎片 + 觉醒石 + 完成神话任务
    def can_awaken_mythic(self, eid: str) -> bool:
        eq = self.equipment.get(eid)
        if eq is None or eq.is_mythic:
            return False
        return (
            eq.quality == "legendary"
            and eq.level >= MAX_EQUIP_LEVEL
            and eq.mythic_shards >= AWAKEN_SHARDS_REQUIRED
            and eq.awakening_stones >= AWAKEN_STONES_REQUIRED
            and eq.quest_completed
        )

    # bug2: 技能按神话类型区分，每个神话有独有终极技能和被动
    def get_mythic_skill(self, mythic_type: str) -> str:
        skills = MYTHIC_SKILLS.get(mythic_type)
        if skills is None:
            return ""
        return skills["ultimate"]

    def get_mythic_passive(self, mythic_type: str) -> str:
        skills = MYTHIC_SKILLS.get(mythic_type)
        if skills is None:
            return ""
        return skills["passive"]

    # bug3: 突破分10阶，只能逐阶突破，不能跳阶
    def can_breakthrough_stage(self, current_stage: int, target_stage: int) -> bool:
        if current_stage < 0 or target_stage > MAX_MYTHIC_STAGE:
            return False
        return target_stage == current_stage + 1

    def get_stage_materials(self, stage: int) -> dict:
        return dict(STAGE_MATERIALS.get(stage, {}))

    # bug4: 套装按神话ID分组，同ID达到数量才触发
    def check_mythic_set(self, items: list) -> dict:
        counts: dict[str, int] = {}
        for item in items:
            mid = item.get("mythic_id", "") if isinstance(item, dict) else getattr(item, "mythic_id", "")
            if mid:
                counts[mid] = counts.get(mid, 0) + 1
        bonuses = {}
        for mid, count in counts.items():
            if count >= SET_BONUS_THRESHOLD:
                bonuses[mid] = f"{count}piece"
        return bonuses

    # bug5: 传承按比例继承（默认50%），高阶损耗更大
    def get_mythic_legacy_rate(self, stage: int = 1) -> float:
        rate = BASE_LEGACY_RATE - LEGACY_STAGE_DECAY * max(0, stage - 1)
        return max(0.1, rate)

    # bug6: 幻化需要通过神话任务或成就解锁
    def is_mythic_illusion_unlocked(self, illusion_id: str) -> bool:
        return illusion_id in self.unlocked_illusions

    def unlock_illusion_by_quest(self, illusion_id: str, quest_id: str) -> bool:
        if quest_id in self.completed_quests:
            self.unlocked_illusions.add(illusion_id)
            return True
        return False

    def unlock_illusion_by_achievement(self, illusion_id: str, achievement_id: str) -> bool:
        if achievement_id in self.achievements:
            self.unlocked_illusions.add(illusion_id)
            return True
        return False

    # bug7: 部位限制，只能同部位觉醒
    def can_awaken_mythic_slot(self, from_slot: str, to_slot: str) -> bool:
        return from_slot == to_slot

    # bug8: 突破有成功率（越阶越低），失败降级，连续失败有保底
    def get_mythic_breakthrough_rate(self, stage: int) -> float:
        return STAGE_BREAKTHROUGH_RATES.get(stage, 0.0)

    def breakthrough(self, eid: str) -> bool:
        import random
        eq = self.equipment.get(eid)
        if eq is None or not eq.is_mythic:
            return False
        target = eq.mythic_stage + 1
        if not self.can_breakthrough_stage(eq.mythic_stage, target):
            return False
        rate = self.get_mythic_breakthrough_rate(target)
        if eq.breakthrough_failures >= GUARANTEE_THRESHOLD:
            rate = 1.0
        if random.random() < rate:
            eq.mythic_stage = target
            eq.breakthrough_failures = 0
            return True
        eq.breakthrough_failures += 1
        if eq.mythic_stage > 1:
            eq.mythic_stage -= 1
        return False

    # bug9: 共鸣按阶数计算，高阶远强于低阶
    def get_resonance_by_stage(self, stage: int) -> float:
        if stage < 1:
            return 0.0
        return round(0.1 * stage * stage, 4)

    # bug10: 神话装备有专属剧情线和任务链，完成才能觉醒和升级
    def needs_mythic_quest(self, eid: str) -> bool:
        eq = self.equipment.get(eid)
        if eq is None or eq.is_mythic:
            return False
        return eq.quality == "legendary" and not eq.quest_completed

    def get_quest_chain(self, mythic_type: str) -> list:
        return list(MYTHIC_QUEST_CHAINS.get(mythic_type, []))

    def complete_quest(self, eid: str, quest_id: str) -> bool:
        eq = self.equipment.get(eid)
        if eq is None:
            return False
        chain = MYTHIC_QUEST_CHAINS.get(eq.mythic_type, [])
        if quest_id not in chain:
            return False
        self.completed_quests.add(quest_id)
        if all(q in self.completed_quests for q in chain):
            eq.quest_completed = True
        return True
