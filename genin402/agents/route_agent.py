import os
from ..models import ShadowTransfer


class RouteAgent:
    """Scores shadow_depth — layering complexity and mixing effectiveness."""

    def score(self, t: ShadowTransfer) -> float:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            try:
                return self._llm_score(t, api_key)
            except Exception:
                pass
        return self._heuristic_score(t)

    def _heuristic_score(self, t: ShadowTransfer) -> float:
        s = 35.0

        # layering: hops × pools = combinatorial complexity
        depth = t.hop_count * max(t.mixer_pools_used, 1)
        s += min(depth * 3, 30)

        # splits add graph branching
        s += min(t.route_splits * 4, 16)

        # dummy outputs expand the UTXO search space
        s += min(t.dummy_outputs * 2, 12)

        # trivial depth penalty
        if t.hop_count <= 1 and t.mixer_pools_used == 0:
            s -= 20

        return max(0.0, min(100.0, s))

    def _llm_score(self, t: ShadowTransfer, api_key: str) -> float:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        prompt = (
            f"Solana privacy transfer shadow depth analysis:\n"
            f"- hop_count: {t.hop_count}\n"
            f"- mixer_pools_used: {t.mixer_pools_used}\n"
            f"- route_splits: {t.route_splits}\n"
            f"- dummy_outputs: {t.dummy_outputs}\n"
            f"Rate shadow depth (layering complexity) 0-100. Reply with only the number."
        )
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=8,
            messages=[{"role": "user", "content": prompt}],
        )
        return max(0.0, min(100.0, float(msg.content[0].text.strip())))
