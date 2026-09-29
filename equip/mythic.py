"""装备神话与超越系统"""
from dataclasses import dataclass, field

MAX_STAGE = 10
AWAKEN_REQUIRED_LEVEL = 60
AWAKEN_REQUIRED_QUALITY = "legendary"
AWAKEN_MATERIALS = {"mythic_shard": 10, "awaken_stone": 5}
BASE_LEGACY_RATE = 0.5
LEGACY_STAGE_PENALTY = 0.03
BREAKTHROUGH_BASE_RATE = 0.95
BREAKTHROUGH_STAGE_DECAY = 0.08
BREAKTHROUGH_FLOOR = 0.10
RESONANCE_PER_STAGE = 0.1

MYTHIC_SKILLS = {
    "destruction": {"ultimate": "annihilation_strike", "passive": "wrath_of_ruin"},
    "protection": {"ultimate": "aegis_of_eternity", "passive": "guardian_bulwark"},
    "swiftness": {"ultimate": "tempest_dash", "passive": "wind_blessing"},
    "wisdom": {"ultimate": "arcane_revelation", "passive": "sage_insight"},
}

SET_THRESHOLDS = {3: "3piece", 5: "5piece"}

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

class MythicSystem:
    def __init__(self):
        self.equipment: dict[str, Equipment] = {}
        self.mythic_tasks: dict = {}
        self.completed_quests: set = set()
        self.unlocked_illusions: set = set()
        self.materials: dict = {}
        self.breakthrough_pity: dict = {}

    def can_awaken_mythic(self, eid: str) -> bool:
        equip = self.equipment.get(eid)
        if equip is None or equip.is_mythic:
            return False
        if equip.quality != AWAKEN_REQUIRED_QUALITY:
            return False
        if equip.level < AWAKEN_REQUIRED_LEVEL:
            return False
        for mat, count in AWAKEN_MATERIALS.items():
            if self.materials.get(mat, 0) < count:
                return False
        return f"mythic_quest_{eid}" in self.completed_quests

    def get_mythic_skill(self, mythic_type: str) -> str:
        skills = MYTHIC_SKILLS.get(mythic_type)
        if skills is None:
            return ""
        return skills["ultimate"]

    def can_breakthrough_stage(self, current_stage: int, target_stage: int) -> bool:
        if not 0 <= current_stage < MAX_STAGE:
            return False
        return target_stage == current_stage + 1

    def check_mythic_set(self, items: list) -> dict:
        counts: dict = {}
        for item in items:
            mid = item.get("mythic_id", "")
            if mid:
                counts[mid] = counts.get(mid, 0) + 1
        for mid, count in counts.items():
            for threshold in sorted(SET_THRESHOLDS, reverse=True):
                if count >= threshold:
                    return {"mythic_id": mid, "bonus": SET_THRESHOLDS[threshold]}
        return {}

    def get_mythic_legacy_rate(self, stage: int = 1) -> float:
        rate = BASE_LEGACY_RATE - LEGACY_STAGE_PENALTY * max(0, stage - 1)
        return max(0.1, rate)

    def is_mythic_illusion_unlocked(self, illusion_id: str) -> bool:
        return illusion_id in self.unlocked_illusions

    def can_awaken_mythic_slot(self, from_slot: str, to_slot: str) -> bool:
        return from_slot == to_slot

    def get_mythic_breakthrough_rate(self, stage: int) -> float:
        pity = self.breakthrough_pity.get(stage, 0)
        rate = BREAKTHROUGH_BASE_RATE - BREAKTHROUGH_STAGE_DECAY * (stage - 1) + pity * 0.05
        return min(1.0, max(BREAKTHROUGH_FLOOR, rate))

    def get_resonance_by_stage(self, stage: int) -> float:
        return RESONANCE_PER_STAGE * max(0, stage)

    def needs_mythic_quest(self, eid: str) -> bool:
        return f"mythic_quest_{eid}" not in self.completed_quests
