import pytest
from genin402.models import ShadowTransfer
from genin402.analyzers.shadow_analyzer import ShadowAnalyzer, _SHADOW_PATTERNS
from genin402.analyzers.route_analyzer import RouteAnalyzer
from genin402.analyzers.shield_analyzer import ShieldAnalyzer


def transfer(**kw) -> ShadowTransfer:
    d = dict(
        wallet_address="AnalyzerWallet",
        transfer_amount_sol=10.0,
        hop_count=6, mixer_pools_used=3,
        decoy_tx_count=12, payment_gate_active=1,
        route_splits=4, time_delay_blocks=30,
        dummy_outputs=6, memo_obfuscated=1,
        token_program_obscured=1, fee_randomized=1,
    )
    d.update(kw)
    return ShadowTransfer(**d)


class TestShadowAnalyzer:
    def setup_method(self): self.a = ShadowAnalyzer()

    def test_returns_float(self):   assert isinstance(self.a.score(transfer()), float)
    def test_range(self):           assert 0.0 <= self.a.score(transfer()) <= 100.0
    def test_10_patterns(self):     assert len(_SHADOW_PATTERNS) == 10

    def test_all_patterns_match(self):
        s = self.a.score(transfer())
        assert s == 100.0

    def test_no_patterns_match(self):
        s = self.a.score(transfer(
            hop_count=1, mixer_pools_used=0, decoy_tx_count=0,
            payment_gate_active=0, route_splits=0, time_delay_blocks=0,
            dummy_outputs=0, memo_obfuscated=0,
            token_program_obscured=0, fee_randomized=0,
        ))
        assert s == 0.0

    def test_partial_match(self):
        s = self.a.score(transfer(
            hop_count=1, mixer_pools_used=0, decoy_tx_count=0,
            payment_gate_active=1, route_splits=0, time_delay_blocks=0,
            dummy_outputs=0, memo_obfuscated=1,
            token_program_obscured=0, fee_randomized=1,
        ))
        assert s == 30.0   # gate_active + memo_dark + fee_noise

    def test_active_shadows_list(self):
        assert isinstance(self.a.active_shadows(transfer()), list)

    def test_active_shadows_not_empty(self):
        assert len(self.a.active_shadows(transfer())) > 0

    def test_multi_hop_pattern(self):
        assert "multi_hop" in self.a.active_shadows(transfer(hop_count=5))

    def test_no_multi_hop(self):
        assert "multi_hop" not in self.a.active_shadows(transfer(hop_count=3))

    def test_flags_exposed(self):
        flags = self.a.shadow_flags(transfer(
            hop_count=1, mixer_pools_used=0, payment_gate_active=0,
            decoy_tx_count=0, memo_obfuscated=0,
        ))
        assert len(flags) > 0

    def test_flags_clean_empty(self):
        flags = self.a.shadow_flags(transfer(
            hop_count=6, mixer_pools_used=3, payment_gate_active=1,
            decoy_tx_count=12, memo_obfuscated=1,
        ))
        assert len(flags) == 0


class TestRouteAnalyzer:
    def setup_method(self): self.a = RouteAnalyzer()

    def test_returns_float(self):   assert isinstance(self.a.score(transfer()), float)
    def test_range(self):           assert 0.0 <= self.a.score(transfer()) <= 100.0

    def test_high_hops_boost(self):
        low  = self.a.score(transfer(hop_count=1))
        high = self.a.score(transfer(hop_count=8))
        assert high > low

    def test_splits_boost(self):
        low  = self.a.score(transfer(route_splits=0))
        high = self.a.score(transfer(route_splits=6))
        assert high > low

    def test_delay_boost(self):
        low  = self.a.score(transfer(time_delay_blocks=0))
        high = self.a.score(transfer(time_delay_blocks=60))
        assert high > low

    def test_single_hop_penalized(self):
        v = self.a.score(transfer(hop_count=1, route_splits=0, time_delay_blocks=0))
        assert v < 20

    def test_flags_no_hops(self):
        flags = self.a.route_flags(transfer(hop_count=1))
        assert any("hop" in f.lower() for f in flags)

    def test_flags_no_splits(self):
        flags = self.a.route_flags(transfer(route_splits=0))
        assert any("split" in f.lower() for f in flags)

    def test_flags_clean_empty(self):
        flags = self.a.route_flags(transfer(hop_count=6, route_splits=4, time_delay_blocks=30))
        assert len(flags) == 0


class TestShieldAnalyzer:
    def setup_method(self): self.a = ShieldAnalyzer()

    def test_returns_float(self):   assert isinstance(self.a.score(transfer()), float)
    def test_range(self):           assert 0.0 <= self.a.score(transfer()) <= 100.0

    def test_gate_active_boosts(self):
        off = self.a.score(transfer(payment_gate_active=0))
        on  = self.a.score(transfer(payment_gate_active=1))
        assert on > off

    def test_pools_boost(self):
        low  = self.a.score(transfer(mixer_pools_used=0))
        high = self.a.score(transfer(mixer_pools_used=5))
        assert high > low

    def test_no_shield_penalized(self):
        v = self.a.score(transfer(
            payment_gate_active=0, mixer_pools_used=0,
            fee_randomized=0, dummy_outputs=0,
            memo_obfuscated=0, token_program_obscured=0,
        ))
        assert v < 30

    def test_fee_randomized_boosts(self):
        off = self.a.score(transfer(fee_randomized=0))
        on  = self.a.score(transfer(fee_randomized=1))
        assert on > off

    def test_flags_no_gate(self):
        flags = self.a.shield_flags(transfer(payment_gate_active=0))
        assert any("402" in f or "gate" in f.lower() for f in flags)

    def test_flags_no_pools(self):
        flags = self.a.shield_flags(transfer(mixer_pools_used=0))
        assert any("mixer" in f.lower() or "pool" in f.lower() for f in flags)

    def test_flags_clean_empty(self):
        flags = self.a.shield_flags(transfer(
            payment_gate_active=1, mixer_pools_used=3,
            fee_randomized=1, dummy_outputs=6,
        ))
        assert len(flags) == 0
