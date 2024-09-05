from dataclasses import dataclass
from enum import Enum


class Genin402Verdict(str, Enum):
    ANBU     = "ANBU"
    JONIN    = "JONIN"
    CHUNIN   = "CHUNIN"
    GENIN    = "GENIN"
    ACADEMY  = "ACADEMY"
    CIVILIAN = "CIVILIAN"


@dataclass
class ShadowTransfer:
    wallet_address: str
    transfer_amount_sol: float
    hop_count: int
    mixer_pools_used: int
    decoy_tx_count: int
    payment_gate_active: int      # 0 or 1
    route_splits: int
    time_delay_blocks: int
    dummy_outputs: int
    memo_obfuscated: int          # 0 or 1
    token_program_obscured: int   # 0 or 1
    fee_randomized: int           # 0 or 1


@dataclass
class Genin402Metrics:
    stealth_score: float     # weight 0.25
    route_entropy: float     # weight 0.25
    payment_shield: float    # weight 0.20
    trace_resistance: float  # weight 0.20
    shadow_depth: float      # weight 0.10

    WEIGHTS: dict = None

    def __post_init__(self):
        object.__setattr__(self, "WEIGHTS", {
            "stealth_score":    0.25,
            "route_entropy":    0.25,
            "payment_shield":   0.20,
            "trace_resistance": 0.20,
            "shadow_depth":     0.10,
        })

    def weighted_score(self) -> float:
        return (
            self.stealth_score    * 0.25 +
            self.route_entropy    * 0.25 +
            self.payment_shield   * 0.20 +
            self.trace_resistance * 0.20 +
            self.shadow_depth     * 0.10
        )


@dataclass
class ShadowReport:
    op_id: str
    wallet_address: str
    verdict: Genin402Verdict
    privacy_score: float
    cloak_status: str        # "dark"|"grey"|"dim"|"exposed"
    metrics: Genin402Metrics
    shadows: list            # active shadow pattern names
    timestamp: float
