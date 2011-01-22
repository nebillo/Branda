from google.appengine.ext import db
from google.appengine.ext.db import polymodel
import datetime


class Venue(polymodel.PolyModel):
    facebook_id = db.StringProperty(required = True)
    created_at = db.DateTimeProperty(required = True, auto_now_add = True)
    updated_at = db.DateTimeProperty(required = True, auto_now = True)
    
    location = db.GeoPtProperty(required = True)
    target_age = db.FloatProperty()
    people = db.IntegerProperty(required = True, default = 0)


class Place(Venue):
    name = db.StringProperty(required = True)


class Event(Venue):
    name = db.StringProperty(required = True)
    description = db.StringProperty()
    picture_url = db.LinkProperty()
    period = db.ListProperty(datetime.datetime)
    
    venue_name = db.StringProperty(required = True)
    address = db.PostalAddressProperty()
    country = db.StringProperty()
    
    
    def startTime(self):
        if len(self.period) > 0:
            return self.period[0]
        return None
    
    def endTime(self):
        if len(self.period) > 1:
            return self.period[1]
        return self.startTime()
