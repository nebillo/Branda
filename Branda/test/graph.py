import unittest
from model.graph import *
from libs import iso8601
import logging


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
        updater.updateUserBasicInfo(info)
        
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
    
    def test_stream(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        updater = GraphUpdater(user)
        
        places = [{
            "created_time": "2011-02-01T22:02:50+0000"
        },
        {
            "created_time": "2010-10-10T19:52:42+0000"
        },
        {
            "created_time": "2010-10-09T21:56:11+0000"
        },
        {
            "created_time": "2010-10-02T22:12:52+0000"
        },
        {
            "created_time": "2010-09-18T19:19:16+0000"
        }]
        events = [{
            "start_time": "2012-02-06T06:00:00+0000"
        },
        {
            "start_time": "2011-02-04T05:30:00+0000"
        },
        {
            "start_time": "2010-01-24T02:00:00+0000"
        }]
        likes = [{
            "created_time": "2012-01-19T12:56:01+0000"
        },
        {
            "created_time": "2011-01-12T12:30:55+0000"
        },
        {
            "created_time": "2010-01-12T00:22:53+0000"
        }]
        
        merged = updater.getStreamByMergingData(likes, events, places)
        self.assertEqual(merged[0]["type"], GraphUpdater.kEventType)
        self.assertTrue(merged[0]["start_time"], "2012-02-06T06:00:00+0000")
        self.assertEqual(merged[-1]["type"], GraphUpdater.kPageType)
        self.assertTrue(merged[-1]["created_time"], "2010-01-12T00:22:53+0000")
    
    def test_page_from_data(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        updater = GraphUpdater(user)
        
        data = {
            "name": "sabato sera teenager", 
            "id": "xxx", 
            "category": "other", 
            "picture": "http://saturday/teen.jpg"
        }
        page = updater.pageFromData(data)
        
        self.assertTrue(isinstance(page, Page))
        self.assertEqual(page.facebook_id, "xxx")
        self.assertEqual(page.name, "sabato sera teenager")
        self.assertEqual(page.category, "other")
        self.assertEqual(page.picture_url, "http://saturday/teen.jpg")
        
        same_page = updater.pageFromData(data)
        self.assertEqual(page.key(), same_page.key())
        
    def test_place_from_data(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        updater = GraphUpdater(user)
        
        data = {
            "name": "the box", 
            "id": "place-id", 
            "location": {"latitude": 12.22, "longitude": 34.55},
        }
        data = {"id": "check-in id", "place": data}
        
        place = updater.placeFromData(data)
        self.assertTrue(isinstance(place, Place))
        self.assertEqual(place.facebook_id, "place-id")
        self.assertEqual(place.name, "the box")
        self.assertEqual(place.location.lat, 12.22)
        self.assertEqual(place.location.lon, 34.55)
        
        same_place = updater.placeFromData(data)
        self.assertEqual(place.key(), same_place.key())
        
    def test_event_from_data(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        updater = GraphUpdater(user)
        
        venue = {
            "latitude": 12.22, 
            "longitude": 34.55,
            "street": "street",
            "city": "city",
            "zip": "zip",
            "state": "state",
            "country": "it"
        }
        data = {
            "name": "pugni e peae",
            "description": "tutti quanti i se copa de pugni",
            "id": "xxx", 
            "location": "casa de luca",
            "venue": venue,
            "start_time": "2011-01-12T22:30:55+0000",
            "end_time": "2011-02-12T04:30:55+0000",
            "picture": "http://luca.com"
        }
        
        event = updater.eventFromData(data)
        self.assertTrue(isinstance(event, Event))
        self.assertEqual(event.facebook_id, "xxx")
        self.assertEqual(event.location.lat, 12.22)
        self.assertEqual(event.location.lon, 34.55)
        self.assertEqual(event.name, "pugni e peae")
        self.assertEqual(event.description, "tutti quanti i se copa de pugni")
        self.assertEqual(event.picture_url, "http://luca.com")
        self.assertEqual(event.venue_name, "casa de luca")
        self.assertEqual(event.country, "it")
        self.assertEqual(event.address, "street, city, zip, state")
        self.assertEqual(event.startTime().strftime("%H:%M"), "22:30")
        self.assertEqual(event.endTime().strftime("%H:%M"), "04:30")
        
    