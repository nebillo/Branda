import unittest
from model.user import User
import datetime


class UserTests(unittest.TestCase):
    def test_age(self):
        user = User(facebook_id = "fake", facebook_access_token = "fake")
        
        today = datetime.date.today()
        years = datetime.timedelta(days = 365 * 23)
        # forever 23
        user.birthday = today - years
        self.assertEqual(round(user.age), 23)