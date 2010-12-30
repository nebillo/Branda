from google.appengine.ext import db
import datetime


class BAUser(db.Model):
    # identification
    facebook_id = db.StringProperty(required = True)
    facebook_access_token = db.StringProperty(required = True)
    created_at = db.DateTimeProperty(required = True)
    updated_at = db.DateTimeProperty()
    
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
    
    # likes
    
    # events
    
    # places
    
    def needsUpdate(self):
        if not self.updated_at:
            return True
        # check updated_at
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
        
        self.put()
    
        
    def updateLikes(self, likes):
        #TOOD: implement
        
        self.put()
        
          
    def updateEvents(self, events):
        #TOOD: implement
        
        self.put()
    
    
    def updatePlaces(self, places):
        #TOOD: implement
        
        self.put()
        