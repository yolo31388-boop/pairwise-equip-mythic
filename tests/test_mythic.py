"""装备神话与超越系统 - 红态测试"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from equip.mythic import MythicSystem, Equipment

class TestAwakenCondition:
    def test_common_equip_cannot_awaken_mythic(self):
        ms = MythicSystem()
        ms.equipment["e1"] = Equipment("e1", "sword", level=1, quality="common")
        assert ms.can_awaken_mythic("e1") == False

class TestMythicSkill:
    def test_different_mythic_types_different_skills(self):
        ms = MythicSystem()
        s1 = ms.get_mythic_skill("destruction")
        s2 = ms.get_mythic_skill("protection")
        assert s1 != s2

class TestStageRestriction:
    def test_cannot_skip_stages(self):
        ms = MythicSystem()
        assert ms.can_breakthrough_stage(1, 5) == False
        assert ms.can_breakthrough_stage(1, 2) == True

class TestMythicSetById:
    def test_mixed_mythic_items_dont_trigger_set(self):
        ms = MythicSystem()
        items = [{"mythic_id": "A"}, {"mythic_id": "A"}, {"mythic_id": "B"}]
        result = ms.check_mythic_set(items)
        assert result == {}

class TestMythicLegacyRate:
    def test_mythic_legacy_is_not_full(self):
        ms = MythicSystem()
        rate = ms.get_mythic_legacy_rate()
        assert rate < 1.0

class TestMythicIllusion:
    def test_special_illusion_not_default(self):
        ms = MythicSystem()
        assert ms.is_mythic_illusion_unlocked("mythic_illusion_x") == False

class TestSlotRestriction:
    def test_weapon_mythic_cannot_awaken_armor(self):
        ms = MythicSystem()
        assert ms.can_awaken_mythic_slot("weapon", "armor") == False

class TestBreakthroughRate:
    def test_high_stage_breakthrough_can_fail(self):
        ms = MythicSystem()
        r1 = ms.get_mythic_breakthrough_rate(1)
        r10 = ms.get_mythic_breakthrough_rate(10)
        assert r10 < r1

class TestResonanceByStage:
    def test_high_stage_resonance_stronger(self):
        ms = MythicSystem()
        r1 = ms.get_resonance_by_stage(1)
        r10 = ms.get_resonance_by_stage(10)
        assert r10 > r1

class TestMythicQuest:
    def test_mythic_awakening_needs_quest(self):
        ms = MythicSystem()
        ms.equipment["e1"] = Equipment("e1", "sword", level=60, quality="legendary")
        assert ms.needs_mythic_quest("e1") == True
