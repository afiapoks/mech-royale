"""Fast survival steering. These are hypotheses to measure in real matches."""
import math
from collections import deque


def unit(dx, dy):
    length = math.hypot(dx, dy)
    return (dx / length, dy / length) if length > 0.001 else (0.0, 0.0)


class Navigator:
    def __init__(self, config):
        self.config = config["mech"]
        self.history = deque()
        self.last_move = (0.0, 0.0)

    def decide(self, obs):
        me, zone = obs["self"], obs["zone"]
        x, y, _ = me["pos"]
        now = obs["t"]
        stats = me["stats"]
        speed = stats.get("walk_speed", self.config["walk_speed"])
        radius = stats.get("radius", self.config["radius"])
        margin = radius + 8.0
        current_radius = max(0.0, zone["radius"] - margin)
        next_radius = max(0.0, zone["next_radius"] - margin)
        center, future = zone["center"], zone["next_center"]
        distance_now = math.hypot(x - center[0], y - center[1])
        distance_next = math.hypot(x - future[0], y - future[1])
        remaining = max(0.0, zone["shrink_end"] - now)
        travel = max(0.0, distance_next - next_radius) / max(speed, 0.1)
        # Start relocating before the circle closes. A time buffer allows detours.
        urgent = travel + 8.0 >= remaining
        escaping_zone = not me["in_zone"] or distance_now > current_radius

        self.history.append((now, x, y))
        while self.history and now - self.history[0][0] > 2.0:
            self.history.popleft()
        oldest = self.history[0]
        stuck = (now - oldest[0] >= 1.5
                 and math.hypot(x - oldest[1], y - oldest[2]) < 1.0
                 and math.hypot(*self.last_move) > 0.5)

        enemies = [m for m in obs["mechs"] if m["kind"] == "mech"]
        near = [m for m in enemies if math.dist(m["pos"][:2], (x, y)) < 160.0]
        target = center if escaping_zone else future
        toward = unit(target[0] - x, target[1] - y)
        candidates = [toward]
        candidates += [(math.cos(i * math.tau / 16), math.sin(i * math.tau / 16))
                       for i in range(16)]
        # When safe and undisturbed, standing still conserves energy and allows healing.
        if not near and not escaping_zone and distance_next <= next_radius:
            candidates.append((0.0, 0.0))

        boost = (escaping_zone or (urgent and travel > remaining)) and me["energy"] > 15
        if boost:
            speed = stats.get("boost_speed", self.config["boost_speed"])
        horizon = 1.2

        def cost(move):
            px, py = x + move[0] * speed * horizon, y + move[1] * speed * horizon
            dc = math.hypot(px - center[0], py - center[1])
            dn = math.hypot(px - future[0], py - future[1])
            # A metre outside the playable area costs far more than enemy spacing.
            score = 40.0 * max(0.0, dc - current_radius)
            if escaping_zone:
                score += 8.0 * dc
            score += (12.0 if urgent else 0.04) * max(0.0, dn - next_radius)
            for enemy in near:
                ex = enemy["pos"][0] + enemy["vel"][0] * horizon
                ey = enemy["pos"][1] + enemy["vel"][1] * horizon
                score += 700.0 / (math.hypot(px - ex, py - ey) + 10.0)
            score += 0.3 * math.hypot(*move)
            # Prefer consistent direction, except when we appear blocked.
            dot = move[0] * self.last_move[0] + move[1] * self.last_move[1]
            score += (5.0 if stuck else -0.2) * dot
            return score

        move = min(candidates, key=cost)
        self.last_move = move
        # Repeated periodic jumps waste energy; jump only to escape a suspected obstruction.
        jump = stuck and me["grounded"] and me["energy"] > 30
        if stuck and not me["grounded"] and me["energy"] > 30:
            boost = True
        return {"move": list(move), "boost": boost, "jump": jump}
