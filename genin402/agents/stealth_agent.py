import os
from ..models import ShadowTransfer


class StealthAgent:
    """Scores trace_resistance — how hard the transfer is to follow on-chain."""

    def score(self, t: ShadowTransfer) -> float:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            try:
                return self._llm_score(t, api_key)
            except Exception:
                pass
        return self._heuristic_score(t)

    def _heuristic_score(self, t: ShadowTransfer) -> float:
        s = 40.0

        # decoy transactions drown the real one in noise
        s += min(t.decoy_tx_count * 3, 24)

        # obfuscation layers compound
        s += t.memo_obfuscated * 8
        s += t.token_program_obscured * 8
        s += t.fee_randomized * 6

        # large amounts are inherently more traceable
        if t.transfer_amount_sol > 500:
            s -= 15
        elif t.transfer_amount_sol > 100:
            s -= 8
        elif t.transfer_amount_sol < 1:
            s -= 5   # micro-amounts are suspicious too

        # no obfuscation at all
        if (t.memo_obfuscated == 0 and t.token_program_obscured == 0
                and t.fee_randomized == 0):
            s -= 15

        return max(0.0, min(100.0, s))

    def _llm_score(self, t: ShadowTransfer, api_key: str) -> float:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        prompt = (
            f"Solana privacy transfer trace resistance analysis:\n"
            f"- decoy_tx_count: {t.decoy_tx_count}\n"
            f"- memo_obfuscated: {t.memo_obfuscated}\n"
            f"- token_program_obscured: {t.token_program_obscured}\n"
            f"- fee_randomized: {t.fee_randomized}\n"
            f"- transfer_amount_sol: {t.transfer_amount_sol}\n"
            f"Rate trace resistance 0-100. Reply with only the number."
        )
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=8,
            messages=[{"role": "user", "content": prompt}],
        )
        return max(0.0, min(100.0, float(msg.content[0].text.strip())))
