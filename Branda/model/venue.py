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

    def updateTargetAgeWithUser(self, user):
        """
        aggiorna l'eta' media della venue con quella dell'utente
        basandosi sulla sommatoria di tutte le eta' delle persone
        """
        age = user.age;
        if not age:
            return
            
        if self.people == 0:
            self.target_age = age
        else:
            self.target_age = (self.target_age * self.people + age) / (self.people + 1)
        self.people += 1
        self.put()
        
        return self.target_age


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
    
    
    def getStartTime(self):
        if len(self.period) > 0:
            return self.period[0]
        return None
    
    def getEndTime(self):
        if len(self.period) > 1:
            return self.period[1]
        return self.startTime()
        
    startTime = property(getStartTime)
    endTime = property(getEndTime)
