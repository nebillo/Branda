from google.appengine.ext import db
import datetime


class BAUser(db.Model):
    # identification
    facebook_id = db.StringProperty(required = True)
    facebook_access_token = db.StringProperty(required = True)
    created_at = db.DateTimeProperty(required = True)
    
    # info
    name = db.StringProperty()
    fullname = db.StringProperty()
    name = db.StringProperty()
    birthdate = db.DateProperty()
    email = db.EmailProperty()
    gender = db.StringProperty(choices = set(["male", "female"]))
    location = db.GeoPtProperty()
    religion = db.StringProperty()
    political = db.StringProperty()
    locale = db.StringProperty()
    info_updated_at = db.DateTimeProperty()
    
    # likes
    likes_updated_at = db.DateTimeProperty()
    
    # events
    events_updated_at = db.DateTimeProperty()
    
    # places
    places_updated_at = db.DateTimeProperty()
    
    
    def needsUpdate(self):
        if self.needsInfoUpdate():
            return True
        if self.needsLikesUpdate():
            return True
        if self.needsEventsUpdate():
            return True
        if self.needsPlacesUpdate():
            return True
        return False
         
    def needsInfoUpdate(self):
        if not self.info_updated_at:
            return True
        # check info_updated_at
        return False
    
    def needsLikesUpdate(self):
        if not self.likes_updated_at:
            return True
        # check likes_updated_at
        return False
    
    def needsEventsUpdate(self):
        if not self.events_updated_at:
            return True
        # check events_updated_at
        return False
    
    def needsPlacesUpdate(self):
        if not self.places_updated_at:
            return True
        # check places_updated_at
        return False
       
     
    def updateInfo(self, values):
        self.name = values["first_name"]
        self.fullname = values["name"]
        self.email = values["email"]
        if "gender" in values:
            self.gender = values["gender"]
        if "political" in values:
            self.political = values["political"]
        if "religion" in values:
            self.religion = values["religion"]
        self.locale = values["locale"]
        
        self.info_updated_at = datetime.datetime.now()
        self.put()
    
        
    def updateLikes(self, likes):
        #TOOD: implement
        
        self.likes_updated_at = datetime.datetime.now()
        self.put()
        
          
    def updateEvents(self, events):
        #TOOD: implement
        
        self.events_updated_at = datetime.datetime.now()
        self.put()
    
    
    def updatePlaces(self, places):
        #TOOD: implement
        
        self.places_updated_at = datetime.datetime.now()
        self.put()
        