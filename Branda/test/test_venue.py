import unittest

from google.appengine.ext import db
import datetime

from model.venue import Venue
from model.user import User


class VenueTests(unittest.TestCase):
    def test_update_target_age(self):
        venue = Venue(facebook_id = "fake", location = db.GeoPt(22,33))
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        today = datetime.date.today()
        
        years = datetime.timedelta(days = 365 * 23)
        user.birthday = today - years
        venue.updateTargetAgeWithUser(user)
        self.assertEqual(round(venue.target_age), 23)
        self.assertEqual(venue.people, 1)
        
        years = datetime.timedelta(days = 365 * 27)
        user.birthday = today - years
        venue.updateTargetAgeWithUser(user)
        self.assertEqual(round(venue.target_age), 25)
        self.assertEqual(venue.people, 2)