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
        self.assertEqual(event.startTime.strftime("%H:%M"), "22:30")
        self.assertEqual(event.endTime.strftime("%H:%M"), "04:30")
        
        same_event = updater.eventFromData(data)
        self.assertEqual(event.key(), same_event.key())
        
    def test_connect_user_to_thing(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        user.put()
        
        page = Page(name = "ci piace luca", facebook_id = "xxx")
        page.put()
        
        updater = GraphUpdater(user)
        linking = updater.connectUserToThing(page, 3)
        self.assertTrue(isinstance(linking, UserLinking))
        self.assertEqual(linking.user, user)
        self.assertEqual(linking.thing, page)
        self.assertEqual(linking.count, 3)
        
        same_linking = updater.connectUserToThing(page)
        self.assertEqual(linking.key(), same_linking.key())
        self.assertEqual(same_linking.count, 4)
        
    def test_add_thing_to_user_list(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        user.put()
        
        page = Page(name = "ci piace luca", facebook_id = "xxx")
        page.put()
        
        updater = GraphUpdater(user)
        things = updater.addThingToUserList(page)
        self.assertTrue(isinstance(things, list))
        self.assertTrue(page.key() in things)
        
        same_things = updater.addThingToUserList(page)
        self.assertEqual(len(same_things), len(things))
        
    def test_add_venue_to_user_list(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        today = datetime.date.today()
        years = datetime.timedelta(days = 365 * 23)
        user.birthday = today - years
        user.put()
        
        place = Place(name = "casa di luca", facebook_id = "xxx", location = db.GeoPt(12.22, 24.44))
        place.put()
        
        updater = GraphUpdater(user)
        venues = updater.addVenueToUserList(place)
        self.assertTrue(isinstance(venues, list))
        self.assertTrue(place.key() in venues)
        self.assertEqual(place.people, 1)
        self.assertEqual(round(place.target_age), 23)
        
        same_venues = updater.addVenueToUserList(place)
        self.assertEqual(len(same_venues), len(venues))
        self.assertEqual(place.people, 1, "ignoring same user")
        
    def test_connect_venue_to_thing(self):
        place = Place(name = "casa di luca", facebook_id = "xxx", location = db.GeoPt(12.22, 24.44))
        place.put()
        
        page = Page(name = "ci piace luca", facebook_id = "xxx")
        page.put()
        
        updater = GraphUpdater(User(facebook_id = "fake", facebook_access_token = "fake"))
        linking = updater.connectVenueToThing(place, page)
        self.assertTrue(isinstance(linking, VenueLinking))
        self.assertEqual(linking.venue, place)
        self.assertEqual(linking.thing, page)
        self.assertEqual(linking.count, 1)
        self.assertFalse(linking.is_active)
        
        same_linking = updater.connectVenueToThing(place, page)
        self.assertEqual(linking.key(), same_linking.key())
        self.assertEqual(same_linking.count, 2)
        
        active_linking = updater.connectVenueToThing(place, page)
        self.assertTrue(active_linking.is_active)
        
    def test_user_active_things(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        user.put()
        
        page = Page(name = "ci piace luca", facebook_id = "xxx")
        page.put()
        
        updater = GraphUpdater(user)
        
        linking = updater.connectUserToThing(thing = page)
        things = updater.getUserActiveThings()
        self.assertTrue(isinstance(things, list))
        self.assertEqual(len(things), 0)
        
        linking.is_active = True
        linking.put()
        things = updater.getUserActiveThings()
        self.assertEqual(len(things), 1)
        self.assertTrue(page.key() in things)
        
        future = datetime.datetime.now() + datetime.timedelta(days = 3)
        things = updater.getUserActiveThings(since_date = future, days = 2)
        self.assertEqual(len(things), 0)
        
    def test_venue_active_things(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        user.put()
        
        place = Place(name = "casa di luca", facebook_id = "xxx", location = db.GeoPt(12.22, 24.44))
        place.put()
        
        page = Page(name = "ci piace luca", facebook_id = "xxx")
        page.put()
        
        updater = GraphUpdater(user)
        
        linking = updater.connectVenueToThing(venue = place, thing = page)
        things = updater.getVenueActiveThings(place)
        self.assertTrue(isinstance(things, list))
        self.assertEqual(len(things), 0)
        
        linking.is_active = True
        linking.put()
        things = updater.getVenueActiveThings(place)
        self.assertEqual(len(things), 1)
        self.assertTrue(page.key() in things)
        
        future = datetime.datetime.now() + datetime.timedelta(days = 3)
        things = updater.getVenueActiveThings(venue = place, since_date = future, days = 2)
        self.assertEqual(len(things), 0)
        
    def test_update_affinity(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        user.put()
        
        place = Place(name = "casa di luca", facebook_id = "xxx", location = db.GeoPt(12.22, 24.44))
        place.put()
        
        updater = GraphUpdater(user)
        
        
        # nothing in common
        thing1 = Page(name = "thing1", facebook_id = "thing1")
        thing1.put()
        updater.connectUserToThing(thing1)
        
        thing2 = Page(name = "thing2", facebook_id = "thing2")
        thing2.put()
        updater.connectVenueToThing(place, thing2)
        
        affinity = updater.updateAffinity(user = user, venue = place)
        self.assertEqual(affinity.value, 0)
        
        # one thing in common with same count
        user_linking_2 = updater.connectUserToThing(thing2)
        
        affinity = updater.updateAffinity(user = user, venue = place)
        self.assertEqual(affinity.value, 1)
        
        # two things in common with the same count
        venue_linking_1 = updater.connectVenueToThing(place, thing1)
        
        affinity = updater.updateAffinity(user = user, venue = place)
        self.assertEqual(affinity.value, 2)
        
        # two things in common, one good and one bad
        user_linking_2.count = -1
        user_linking_2.put()
        
        affinity = updater.updateAffinity(user = user, venue = place)
        self.assertEqual(affinity.value, 0)
        
        # two things in common, both bad
        venue_linking_1.count = -1
        venue_linking_1.put()
        
        affinity = updater.updateAffinity(user = user, venue = place)
        self.assertEqual(affinity.value, -2)
        
        