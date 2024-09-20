import pytest
from genin402.models import (
    ShadowTransfer, Genin402Metrics, ShadowReport, Genin402Verdict
)


def transfer(**kw) -> ShadowTransfer:
    d = dict(
        wallet_address="TestWallet402",
        transfer_amount_sol=10.0,
        hop_count=6, mixer_pools_used=3,
        decoy_tx_count=12, payment_gate_active=1,
        route_splits=4, time_delay_blocks=30,
        dummy_outputs=6, memo_obfuscated=1,
        token_program_obscured=1, fee_randomized=1,
    )
    d.update(kw)
    return ShadowTransfer(**d)


def metrics(**kw) -> Genin402Metrics:
    d = dict(
        stealth_score=70.0, route_entropy=75.0,
        payment_shield=80.0, trace_resistance=65.0, shadow_depth=60.0,
    )
    d.update(kw)
    return Genin402Metrics(**d)


class TestShadowTransfer:
    def test_creates(self):         assert transfer() is not None
    def test_wallet_field(self):    assert transfer().wallet_address == "TestWallet402"
    def test_amount_float(self):    assert isinstance(transfer().transfer_amount_sol, float)
    def test_hop_count_int(self):   assert isinstance(transfer().hop_count, int)
    def test_gate_binary(self):     assert transfer(payment_gate_active=1).payment_gate_active == 1
    def test_gate_off(self):        assert transfer(payment_gate_active=0).payment_gate_active == 0
    def test_memo_binary(self):     assert transfer(memo_obfuscated=0).memo_obfuscated == 0
    def test_fee_binary(self):      assert transfer(fee_randomized=1).fee_randomized == 1
    def test_program_binary(self):  assert transfer(token_program_obscured=0).token_program_obscured == 0


class TestGenin402Metrics:
    def test_weighted_score_returns_float(self):
        assert isinstance(metrics().weighted_score(), float)

    def test_weighted_score_range(self):
        s = metrics().weighted_score()
        assert 0.0 <= s <= 100.0

    def test_all_zero(self):
        m = metrics(stealth_score=0, route_entropy=0,
                    payment_shield=0, trace_resistance=0, shadow_depth=0)
        assert m.weighted_score() == 0.0

    def test_all_hundred(self):
        m = metrics(stealth_score=100, route_entropy=100,
                    payment_shield=100, trace_resistance=100, shadow_depth=100)
        assert m.weighted_score() == 100.0

    def test_weights_sum_to_one(self):
        w = metrics().WEIGHTS
        assert abs(sum(w.values()) - 1.0) < 1e-9

    def test_stealth_weight(self):
        assert metrics().WEIGHTS["stealth_score"] == 0.25

    def test_route_weight(self):
        assert metrics().WEIGHTS["route_entropy"] == 0.25

    def test_shield_weight(self):
        assert metrics().WEIGHTS["payment_shield"] == 0.20

    def test_trace_weight(self):
        assert metrics().WEIGHTS["trace_resistance"] == 0.20

    def test_shadow_weight(self):
        assert metrics().WEIGHTS["shadow_depth"] == 0.10


class TestGenin402Verdict:
    def test_six_tiers(self):
        assert len(Genin402Verdict) == 6

    def test_anbu_value(self):      assert Genin402Verdict.ANBU == "ANBU"
    def test_jonin_value(self):     assert Genin402Verdict.JONIN == "JONIN"
    def test_chunin_value(self):    assert Genin402Verdict.CHUNIN == "CHUNIN"
    def test_genin_value(self):     assert Genin402Verdict.GENIN == "GENIN"
    def test_academy_value(self):   assert Genin402Verdict.ACADEMY == "ACADEMY"
    def test_civilian_value(self):  assert Genin402Verdict.CIVILIAN == "CIVILIAN"
    def test_is_str(self):          assert isinstance(Genin402Verdict.ANBU, str)
