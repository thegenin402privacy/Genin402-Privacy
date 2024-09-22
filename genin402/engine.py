import hashlib
import time

from .models import ShadowTransfer, Genin402Metrics, ShadowReport, Genin402Verdict
from .analyzers.shadow_analyzer import ShadowAnalyzer
from .analyzers.route_analyzer import RouteAnalyzer
from .analyzers.shield_analyzer import ShieldAnalyzer
from .agents.stealth_agent import StealthAgent
from .agents.route_agent import RouteAgent


class PrivacyEngine:
    def __init__(self):
        self._shadow = ShadowAnalyzer()
        self._route  = RouteAnalyzer()
        self._shield = ShieldAnalyzer()
        self._stealth = StealthAgent()
        self._route_agent = RouteAgent()

    def analyze(self, t: ShadowTransfer) -> ShadowReport:
        metrics = Genin402Metrics(
            stealth_score    = self._shadow.score(t),
            route_entropy    = self._route.score(t),
            payment_shield   = self._shield.score(t),
            trace_resistance = self._stealth.score(t),
            shadow_depth     = self._route_agent.score(t),
        )
        score   = metrics.weighted_score()
        verdict = self._verdict(score)
        return ShadowReport(
            op_id          = self._op_id(t.wallet_address),
            wallet_address = t.wallet_address,
            verdict        = verdict,
            privacy_score  = round(score, 2),
            cloak_status   = self._cloak_status(score),
            metrics        = metrics,
            shadows        = self._shadow.active_shadows(t),
            timestamp      = time.time(),
        )

    def analyze_batch(self, targets: list[ShadowTransfer]) -> list[ShadowReport]:
        reports = [self.analyze(t) for t in targets]
        return sorted(reports, key=lambda r: r.privacy_score, reverse=True)

    @staticmethod
    def _op_id(address: str) -> str:
        return hashlib.sha256(address.encode()).hexdigest()[:8].upper()

    @staticmethod
    def _cloak_status(score: float) -> str:
        if score >= 75:
            return "dark"
        if score >= 55:
            return "grey"
        if score >= 35:
            return "dim"
        return "exposed"

    @staticmethod
    def _verdict(score: float) -> Genin402Verdict:
        if score >= 90:
            return Genin402Verdict.ANBU
        if score >= 75:
            return Genin402Verdict.JONIN
        if score >= 60:
            return Genin402Verdict.CHUNIN
        if score >= 40:
            return Genin402Verdict.GENIN
        if score >= 20:
            return Genin402Verdict.ACADEMY
        return Genin402Verdict.CIVILIAN
