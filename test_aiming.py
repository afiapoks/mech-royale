import math
import unittest
from aiming import intercept_time, gun_aim


class InterceptionTests(unittest.TestCase):
    def test_stationary_target(self):
        self.assertAlmostEqual(intercept_time([100, 0, 0], [0, 0, 0], 250), 0.4)

    def test_sideways_target_meets_projectile(self):
        r, v, speed = [100, 0, 0], [0, 20, 0], 250
        t = intercept_time(r, v, speed)
        self.assertGreater(t, 0.4)
        self.assertAlmostEqual(math.sqrt(sum((a + b * t) ** 2 for a, b in zip(r, v))), speed * t)

    def test_target_faster_than_bullet_moving_away(self):
        self.assertIsNone(intercept_time([100, 0, 0], [300, 0, 0], 250))

    def test_equal_speed_approaching(self):
        self.assertAlmostEqual(intercept_time([100, 0, 0], [-250, 0, 0], 250), 0.2)

    def test_aim_leads_sideways_and_accounts_for_body_height(self):
        config = {"mech": {"muzzle_height": 7, "height": 9}, "cubes": {"size_per_cube": 0.05}}
        me = {"pos": [0, 0, 0], "stats": {"muzzle_height": 7},
              "weapons": [{"kind": "gun", "stats": {"speed": 250, "range": 230}}, None]}
        target = {"pos": [100, 0, 0], "vel": [0, 20, 0], "cubes": 0}
        yaw, pitch = gun_aim(me, target, config)
        self.assertGreater(yaw, 0)
        self.assertLess(pitch, 0)
        target["cubes"] = 20
        self.assertGreater(gun_aim(me, target, config)[1], 0)


if __name__ == "__main__":
    unittest.main()
