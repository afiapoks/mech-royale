"""Check survival decisions in focused scenarios, not a replacement for match scores."""
import copy
import unittest
from navigation import Navigator

CONFIG = {"mech": {"walk_speed": 11.7, "boost_speed": 19.5, "radius": 2.5}}


def observation():
    return {"t": 0.0, "self": {"pos": [0, 0, 0], "stats": {}, "energy": 100,
            "in_zone": True, "grounded": True}, "mechs": [],
            "zone": {"center": [0, 0], "radius": 300, "next_center": [0, 0],
                     "next_radius": 200, "shrink_end": 100}}


class SurvivalTests(unittest.TestCase):
    def test_outside_zone_returns_instead_of_chasing_enemy(self):
        obs = observation()
        obs["self"]["pos"] = [320, 0, 0]
        obs["self"]["in_zone"] = False
        move = Navigator(CONFIG).decide(obs)
        self.assertLess(move["move"][0], -0.8)
        self.assertTrue(move["boost"])

    def test_deadline_moves_to_future_zone(self):
        obs = observation()
        obs["zone"].update(next_center=[100, 0], next_radius=20, shrink_end=4)
        move = Navigator(CONFIG).decide(obs)
        self.assertGreater(move["move"][0], 0.8)
        self.assertTrue(move["boost"])

    def test_safe_position_moves_away_from_close_enemy(self):
        obs = observation()
        obs["mechs"] = [{"kind": "mech", "pos": [25, 0, 0], "vel": [-5, 0, 0]}]
        move = Navigator(CONFIG).decide(obs)
        self.assertLess(move["move"][0], -0.8)

    def test_no_threat_in_safe_area_can_rest(self):
        move = Navigator(CONFIG).decide(observation())
        self.assertEqual(move["move"], [0.0, 0.0])
        self.assertFalse(move["jump"])

    def test_stuck_robot_attempts_escape(self):
        obs = observation()
        obs["zone"].update(next_center=[100, 0], next_radius=20, shrink_end=4)
        nav = Navigator(CONFIG)
        for i in range(19):
            current = copy.deepcopy(obs)
            current["t"] = i / 10
            move = nav.decide(current)
        self.assertTrue(move["jump"])


if __name__ == "__main__":
    unittest.main()
