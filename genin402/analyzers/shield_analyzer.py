from ..models import ShadowTransfer


class ShieldAnalyzer:
    def score(self, t: ShadowTransfer) -> float:
        s = 25.0

        # 402 payment gate is the core shield mechanism
        if t.payment_gate_active == 1:
            s += 28

        # mixer pool depth
        s += min(t.mixer_pools_used * 12, 24)

        # fee randomization prevents amount fingerprinting
        if t.fee_randomized == 1:
            s += 10

        # dummy outputs obscure the real recipient
        if t.dummy_outputs >= 8:
            s += 10
        elif t.dummy_outputs >= 5:
            s += 7
        elif t.dummy_outputs >= 2:
            s += 3

        # memo and program obfuscation
        if t.memo_obfuscated == 1:
            s += 5
        if t.token_program_obscured == 1:
            s += 5

        # hard penalty: no gate AND no pools = no shield at all
        if t.payment_gate_active == 0 and t.mixer_pools_used == 0:
            s -= 20

        return max(0.0, min(100.0, s))

    def shield_flags(self, t: ShadowTransfer) -> list[str]:
        flags = []
        if t.payment_gate_active == 0:
            flags.append("402 gate disabled — transfer unprotected")
        if t.mixer_pools_used == 0:
            flags.append("No mixer pools — amount linkability high")
        if t.fee_randomized == 0:
            flags.append("Static fee — amount pattern fingerprintable")
        if t.dummy_outputs < 2:
            flags.append("Insufficient dummy outputs — recipient identifiable")
        return flags
