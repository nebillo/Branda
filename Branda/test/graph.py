import unittest
from model.graph import *
from libs import iso8601


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
    
    def test_compare_iso_dates(self):
        first_date  = iso8601.parse_date("2011-01-12T12:30:55+0000")
        second_date = iso8601.parse_date("2011-02-04T05:30:00+0000")
        self.assertTrue(first_date < second_date)
        
        first_date  = iso8601.parse_date("2012-01-12T12:30:55+0000")
        second_date = iso8601.parse_date("2010-02-04T05:30:00+0000")
        self.assertTrue(first_date > second_date)
        
        first_date  = iso8601.parse_date("2010-01-20T10:30:55+0000")
        second_date = iso8601.parse_date("2010-01-20T12:30:55+02:00")
        self.assertEqual(first_date, second_date)
    
    def test_merge(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        updater = GraphUpdater(user)
        
        first = [{"date": "2011-03-12T00:22:18+0000"}, {"date": "2011-01-12T00:22:18+0000"}]
        second = [{"date2": "2011-04-12T00:22:18+0000"}, {"date2": "2011-02-12T00:22:18+0000"}]
        merge = updater.mergeOrderedArrays(first, "date", second, "date2")
        
        self.assertEquals(merge[0], second[0])
        self.assertEquals(merge[1], first[0])
        self.assertEquals(merge[2], second[1])
        self.assertEquals(merge[3], first[1])
    
    