import unittest


class Checkup(unittest.TestCase):
    def test_true(self):
        self.assertTrue(True)
        
    def test_venue(self):
        from model.venue import Venue
        self.assertTrue(True)

    def test_thing(self):
        from model.thing import Thing
        self.assertTrue(True)
        
    def test_user(self):
        from model.user import User
        self.assertTrue(True)
        
    def test_affinity(self):
        from model.affinity import Affinity, UserLinking, VenueLinking
        self.assertTrue(True)

    def test_graph(self):
        from model.graph import GraphUpdater
        self.assertTrue(True)
        