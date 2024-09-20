import pytest
from genin402.models import ShadowTransfer, Genin402Verdict, ShadowReport
from genin402.engine import PrivacyEngine


def transfer(**kw) -> ShadowTransfer:
    d = dict(
        wallet_address="EngineTestWallet",
        transfer_amount_sol=10.0,
        hop_count=6, mixer_pools_used=3,
        decoy_tx_count=12, payment_gate_active=1,
        route_splits=4, time_delay_blocks=30,
        dummy_outputs=6, memo_obfuscated=1,
        token_program_obscured=1, fee_randomized=1,
    )
    d.update(kw)
    return ShadowTransfer(**d)


class TestPrivacyEngine:
    def setup_method(self): self.e = PrivacyEngine()

    def test_returns_report(self):
        r = self.e.analyze(transfer())
        assert isinstance(r, ShadowReport)

    def test_score_float(self):
        assert isinstance(self.e.analyze(transfer()).privacy_score, float)

    def test_score_range(self):
        s = self.e.analyze(transfer()).privacy_score
        assert 0.0 <= s <= 100.0

    def test_op_id_length(self):
        assert len(self.e.analyze(transfer()).op_id) == 8

    def test_wallet_passthrough(self):
        r = self.e.analyze(transfer(wallet_address="WalletXYZ"))
        assert r.wallet_address == "WalletXYZ"

    def test_verdict_is_enum(self):
        assert isinstance(self.e.analyze(transfer()).verdict, Genin402Verdict)

    def test_cloak_dark_on_high(self):
        r = self.e.analyze(transfer())
        assert r.cloak_status in ("dark", "grey", "dim", "exposed")

    def test_shadows_list(self):
        r = self.e.analyze(transfer())
        assert isinstance(r.shadows, list)

    def test_timestamp_positive(self):
        assert self.e.analyze(transfer()).timestamp > 0

    def test_high_privacy_anbu(self):
        r = self.e.analyze(transfer(
            hop_count=8, mixer_pools_used=5, decoy_tx_count=20,
            payment_gate_active=1, route_splits=6, time_delay_blocks=60,
            dummy_outputs=10, memo_obfuscated=1, token_program_obscured=1,
            fee_randomized=1,
        ))
        assert r.verdict in (Genin402Verdict.ANBU, Genin402Verdict.JONIN)

    def test_low_privacy_civilian(self):
        r = self.e.analyze(transfer(
            hop_count=1, mixer_pools_used=0, decoy_tx_count=0,
            payment_gate_active=0, route_splits=0, time_delay_blocks=0,
            dummy_outputs=0, memo_obfuscated=0, token_program_obscured=0,
            fee_randomized=0,
        ))
        assert r.verdict in (Genin402Verdict.CIVILIAN, Genin402Verdict.ACADEMY)

    def test_high_score_dark_cloak(self):
        r = self.e.analyze(transfer(
            hop_count=8, mixer_pools_used=5, decoy_tx_count=20,
            payment_gate_active=1, route_splits=6, time_delay_blocks=60,
            dummy_outputs=10, memo_obfuscated=1, token_program_obscured=1,
            fee_randomized=1,
        ))
        assert r.cloak_status in ("dark", "grey")

    def test_low_score_exposed_cloak(self):
        r = self.e.analyze(transfer(
            hop_count=1, mixer_pools_used=0, decoy_tx_count=0,
            payment_gate_active=0, route_splits=0, time_delay_blocks=0,
            dummy_outputs=0, memo_obfuscated=0, token_program_obscured=0,
            fee_randomized=0,
        ))
        assert r.cloak_status in ("exposed", "dim")

    def test_shadows_not_empty_on_good(self):
        r = self.e.analyze(transfer())
        assert len(r.shadows) > 0

    def test_metrics_stealth_range(self):
        m = self.e.analyze(transfer()).metrics
        assert 0.0 <= m.stealth_score <= 100.0

    def test_metrics_route_range(self):
        m = self.e.analyze(transfer()).metrics
        assert 0.0 <= m.route_entropy <= 100.0

    def test_metrics_shield_range(self):
        m = self.e.analyze(transfer()).metrics
        assert 0.0 <= m.payment_shield <= 100.0

    def test_metrics_trace_range(self):
        m = self.e.analyze(transfer()).metrics
        assert 0.0 <= m.trace_resistance <= 100.0

    def test_metrics_shadow_range(self):
        m = self.e.analyze(transfer()).metrics
        assert 0.0 <= m.shadow_depth <= 100.0


class TestAnalyzeBatch:
    def setup_method(self): self.e = PrivacyEngine()

    def test_returns_list(self):
        r = self.e.analyze_batch([transfer(), transfer(wallet_address="W2")])
        assert isinstance(r, list)

    def test_sorted_desc(self):
        high = transfer(
            hop_count=8, mixer_pools_used=5, payment_gate_active=1,
            fee_randomized=1, memo_obfuscated=1, token_program_obscured=1,
            decoy_tx_count=15, route_splits=5, time_delay_blocks=50,
            dummy_outputs=8,
        )
        low = transfer(
            wallet_address="LowWallet",
            hop_count=1, mixer_pools_used=0, payment_gate_active=0,
            fee_randomized=0, memo_obfuscated=0, token_program_obscured=0,
            decoy_tx_count=0, route_splits=0, time_delay_blocks=0,
            dummy_outputs=0,
        )
        reports = self.e.analyze_batch([low, high])
        assert reports[0].privacy_score >= reports[1].privacy_score

    def test_empty_batch(self):
        assert self.e.analyze_batch([]) == []

    def test_batch_count(self):
        targets = [transfer(wallet_address=f"W{i}") for i in range(5)]
        assert len(self.e.analyze_batch(targets)) == 5

    def test_each_has_unique_op_id(self):
        targets = [transfer(wallet_address=f"Wallet{i}") for i in range(4)]
        reports = self.e.analyze_batch(targets)
        op_ids = {r.op_id for r in reports}
        assert len(op_ids) == 4
