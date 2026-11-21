"""Predict where a moving target will meet a straight-flying gun bullet."""
import math


def intercept_time(relative, velocity, speed):
    # At impact, the bullet's travel distance equals the target's distance:
    # |relative + velocity * t| = speed * t. Squaring gives a quadratic.
    if speed <= 0:
        return None
    a = sum(v * v for v in velocity) - speed * speed
    b = 2 * sum(r * v for r, v in zip(relative, velocity))
    c = sum(r * r for r in relative)
    if c < 1e-12:
        return 0.0
    if abs(a) < 1e-9:
        if abs(b) < 1e-9:
            return None
        t = -c / b
        return t if t >= 0 else None
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return None
    root = math.sqrt(discriminant)
    times = [t for t in ((-b - root) / (2 * a), (-b + root) / (2 * a)) if t >= 0]
    return min(times) if times else None


def gun_aim(me, target, config):
    muzzle_height = me["stats"].get("muzzle_height", config["mech"]["muzzle_height"])
    # Enemy positions are at their feet. Aim at their body's center, including cube scaling.
    scale = 1 + config["cubes"]["size_per_cube"] * target.get("cubes", 0)
    target_height = config["mech"]["height"] * scale / 2
    relative = [target["pos"][0] - me["pos"][0],
                target["pos"][1] - me["pos"][1],
                target["pos"][2] + target_height - me["pos"][2] - muzzle_height]
    velocity = target["vel"]
    gun = next((w for w in me["weapons"] if w and w["kind"] == "gun"), None)
    if gun:
        speed = gun["stats"]["speed"]
        flight = intercept_time(relative, velocity, speed)
        # Predictions beyond the bullet's range are not useful. Fall back to direct aim.
        if flight is not None and flight * speed <= gun["stats"]["range"]:
            relative = [r + v * flight for r, v in zip(relative, velocity)]
    return [math.atan2(relative[1], relative[0]),
            math.atan2(relative[2], math.hypot(relative[0], relative[1]))]
