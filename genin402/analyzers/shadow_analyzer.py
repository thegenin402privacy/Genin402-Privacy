from ..models import ShadowTransfer

_SHADOW_PATTERNS: dict = {
    "multi_hop":       lambda t: t.hop_count >= 5,
    "pool_routed":     lambda t: t.mixer_pools_used >= 2,
    "decoy_flood":     lambda t: t.decoy_tx_count >= 10,
    "gate_active":     lambda t: t.payment_gate_active == 1,
    "split_route":     lambda t: t.route_splits >= 3,
    "time_shifted":    lambda t: t.time_delay_blocks >= 20,
    "dummy_outputs":   lambda t: t.dummy_outputs >= 5,
    "memo_dark":       lambda t: t.memo_obfuscated == 1,
    "program_masked":  lambda t: t.token_program_obscured == 1,
    "fee_noise":       lambda t: t.fee_randomized == 1,
}


class ShadowAnalyzer:
    def score(self, t: ShadowTransfer) -> float:
        matched = sum(1 for fn in _SHADOW_PATTERNS.values() if fn(t))
        return float(matched * 10)

    def active_shadows(self, t: ShadowTransfer) -> list[str]:
        return [name for name, fn in _SHADOW_PATTERNS.items() if fn(t)]

    def shadow_flags(self, t: ShadowTransfer) -> list[str]:
        flags = []
        if t.hop_count <= 1:
            flags.append("Single-hop transfer — fully traceable on-chain")
        if t.mixer_pools_used == 0:
            flags.append("No mixer pools — direct wallet exposure")
        if t.payment_gate_active == 0:
            flags.append("402 gate inactive — payment path unshielded")
        if t.decoy_tx_count < 3:
            flags.append("Low decoy count — transfer pattern identifiable")
        if t.memo_obfuscated == 0:
            flags.append("Memo field exposed — metadata leaks intent")
        return flags
