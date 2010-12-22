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
    
    
    def isFirstLaunch(self):
        if not self.info_updated_at:
            return True
        return False
    
    def needsToUpdateInfo(self):
        if not self.info_updated_at:
            return True
        return False
        
    def updateWithDictionary(self, values):
        # TODO: update all fields
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
        