from google.appengine.ext import db

class BAUser(db.Model):
    facebook_id = db.StringProperty(required = True)
    facebook_access_token = db.StringProperty(required = True)
    created_at = db.DateTimeProperty(required = True)
    birthdate = db.DateProperty()