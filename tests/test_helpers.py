import hashlib
import pytest
from genin402.engine import PrivacyEngine
from genin402.models import Genin402Verdict


class TestOpId:
    def test_length_eight(self):
        op = PrivacyEngine._op_id("abc")
        assert len(op) == 8

    def test_uppercase(self):
        op = PrivacyEngine._op_id("abc")
        assert op == op.upper()

    def test_deterministic(self):
        assert PrivacyEngine._op_id("wallet1") == PrivacyEngine._op_id("wallet1")

    def test_different_inputs(self):
        assert PrivacyEngine._op_id("wallet1") != PrivacyEngine._op_id("wallet2")

    def test_matches_sha256(self):
        addr = "TestAddr"
        expected = hashlib.sha256(addr.encode()).hexdigest()[:8].upper()
        assert PrivacyEngine._op_id(addr) == expected


class TestCloakStatus:
    def test_dark_at_75(self):      assert PrivacyEngine._cloak_status(75.0) == "dark"
    def test_dark_at_100(self):     assert PrivacyEngine._cloak_status(100.0) == "dark"
    def test_grey_at_55(self):      assert PrivacyEngine._cloak_status(55.0) == "grey"
    def test_grey_at_74(self):      assert PrivacyEngine._cloak_status(74.9) == "grey"
    def test_dim_at_35(self):       assert PrivacyEngine._cloak_status(35.0) == "dim"
    def test_dim_at_54(self):       assert PrivacyEngine._cloak_status(54.9) == "dim"
    def test_exposed_at_34(self):   assert PrivacyEngine._cloak_status(34.9) == "exposed"
    def test_exposed_at_0(self):    assert PrivacyEngine._cloak_status(0.0) == "exposed"


class TestVerdictThresholds:
    def test_anbu_at_90(self):      assert PrivacyEngine._verdict(90.0) == Genin402Verdict.ANBU
    def test_anbu_at_100(self):     assert PrivacyEngine._verdict(100.0) == Genin402Verdict.ANBU
    def test_jonin_at_75(self):     assert PrivacyEngine._verdict(75.0) == Genin402Verdict.JONIN
    def test_jonin_at_89(self):     assert PrivacyEngine._verdict(89.9) == Genin402Verdict.JONIN
    def test_chunin_at_60(self):    assert PrivacyEngine._verdict(60.0) == Genin402Verdict.CHUNIN
    def test_chunin_at_74(self):    assert PrivacyEngine._verdict(74.9) == Genin402Verdict.CHUNIN
    def test_genin_at_40(self):     assert PrivacyEngine._verdict(40.0) == Genin402Verdict.GENIN
    def test_genin_at_59(self):     assert PrivacyEngine._verdict(59.9) == Genin402Verdict.GENIN
    def test_academy_at_20(self):   assert PrivacyEngine._verdict(20.0) == Genin402Verdict.ACADEMY
    def test_academy_at_39(self):   assert PrivacyEngine._verdict(39.9) == Genin402Verdict.ACADEMY
    def test_civilian_at_0(self):   assert PrivacyEngine._verdict(0.0) == Genin402Verdict.CIVILIAN
    def test_civilian_at_19(self):  assert PrivacyEngine._verdict(19.9) == Genin402Verdict.CIVILIAN
