from google.appengine.ext import db
import datetime
import time
from thing import Religion, Political


class User(db.Model):
    facebook_id = db.StringProperty(required = True)
    facebook_access_token = db.StringProperty(required = True)
    created_at = db.DateTimeProperty(required = True, auto_now_add = True)
    updated_at = db.DateTimeProperty()
    
    name = db.StringProperty()
    fullname = db.StringProperty()
    name = db.StringProperty()
    birthdate = db.DateProperty()
    email = db.EmailProperty()
    gender = db.StringProperty(choices = set(["male", "female"]))
    location = db.GeoPtProperty()
    religion = db.ReferenceProperty(Religion)
    political = db.ReferenceProperty(Political)
    locale = db.StringProperty()
    
    things = db.ListProperty(db.Key)
    venues = db.ListProperty(db.Key)
    
    def updatedAtInUnixFormat(self):
        if not self.updated_at:
            return 0.0
        return time.mktime(self.updated_at.timetuple())
    
    def neverUpdated(self):
        if not self.updated_at:
            return True
        return False
    
    def needsUpdate(self):
        if not self.updated_at:
            return True
        # check updated_at
        return False
