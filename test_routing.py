import unittest
from routing import Router

class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.router = Router({'bounds':{'minX':0,'maxX':96,'minY':0,'maxY':96},
                              'prisms':[{'kind':'building','ring':[40,24,56,24,56,72,40,72],'holes':[]}]})
        self.zone = {'center':[48,48],'radius':100}

    def test_routes_around_wall(self):
        path = self.router.search([8,48],[88,48],self.zone)
        self.assertTrue(path)
        self.assertTrue(all(self.router.free(self.router.cell(p)) for p in path))
        self.assertTrue(any(p[1]<24 or p[1]>72 for p in path))
        self.assertEqual(path[-1],(88,48))

    def test_goal_inside_building_ends_on_free_ground(self):
        path = self.router.search([8,48],[48,48],self.zone)
        self.assertTrue(path)
        self.assertTrue(self.router.free(self.router.cell(path[-1])))

    def test_no_route_returns_empty(self):
        self.router.blocked = {(i,j) for i in range(self.router.nx) for j in range(self.router.ny)}
        self.assertEqual(self.router.search([8,48],[88,48],self.zone),[])

if __name__ == '__main__':
    unittest.main()
