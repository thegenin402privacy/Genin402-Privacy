from ..models import ShadowTransfer


class RouteAnalyzer:
    def score(self, t: ShadowTransfer) -> float:
        s = 35.0

        # hop complexity — each hop adds entropy
        s += min(t.hop_count * 7, 35)

        # route splits diversify the path graph
        s += min(t.route_splits * 5, 20)

        # time delay makes chain analysis harder
        if t.time_delay_blocks >= 50:
            s += 12
        elif t.time_delay_blocks >= 20:
            s += 7
        elif t.time_delay_blocks >= 5:
            s += 3

        # penalties for trivial routes
        if t.hop_count <= 1:
            s -= 25
        if t.route_splits == 0:
            s -= 10
        if t.time_delay_blocks == 0:
            s -= 5

        return max(0.0, min(100.0, s))

    def route_flags(self, t: ShadowTransfer) -> list[str]:
        flags = []
        if t.hop_count <= 1:
            flags.append("Hop count too low — route entropy near zero")
        if t.route_splits == 0:
            flags.append("No route splits — linear path trivially traceable")
        if t.time_delay_blocks == 0:
            flags.append("Zero block delay — timing analysis possible")
        return flags
