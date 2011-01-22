import unittest
from model.graph import *


class GraphTests(unittest.TestCase):
    def test_empty_data(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        updater = GraphUpdater(user)
        nodes_updated = updater.updateNodes(info = {}, likes = [], places = [], events = [])
        self.assertFalse(nodes_updated)
        
    def test_basic_info(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        updater = GraphUpdater(user)
        
        info = { 
            "first_name": "luca", 
            "last_name": "milan", 
            "name": "luca milan", 
            "email": "milan@milan", 
            "gender": "female", 
            "locale": "it_IT",
            "birthday": "03/20/1987",
        }
        updater.updateNodes(info = info, likes = [], places = [], events = [])
        
        self.assertEquals(user.first_name, "luca")
        self.assertEquals(user.last_name, "milan")
        self.assertEquals(user.name, "luca milan")
        self.assertEquals(user.email, "milan@milan")
        self.assertEquals(user.gender, "female")
        self.assertEquals(user.locale, "it_IT")
        self.assertEquals(user.birthday.strftime("%m/%d/%Y"), "03/20/1987")