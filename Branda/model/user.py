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
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    birthday = db.DateProperty()
    email = db.EmailProperty()
    gender = db.StringProperty(choices = set(["male", "female"]))
    location = db.GeoPtProperty()
    religion = db.ReferenceProperty(Religion)
    political = db.ReferenceProperty(Political)
    locale = db.StringProperty()
    
    things = db.ListProperty(db.Key)
    venues = db.ListProperty(db.Key)
    
    def getAge(self):
        """
        ritorna gli anni di eta' dell'utente come numero reale
        """
        if not self.birthday:
            return 0.0
        
        today = datetime.date.today()
        period = today - self.birthday
        return (period.days) / 365.0
        
    age = property(getAge)
    
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
