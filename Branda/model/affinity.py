from google.appengine.ext import db
from user import User
from venue import Venue
from thing import Thing


class UserLinking(db.Model):
    user = db.ReferenceProperty(User, required = True, collection_name = 'linked_things')
    thing = db.ReferenceProperty(Thing, required = True, collection_name = 'linked_users')
    count = db.IntegerProperty(required = True, default = 1)
    created_at = db.DateTimeProperty(required = True, auto_now_add = True)
    updated_at = db.DateTimeProperty(required = True, auto_now = True)  
    

class VenueLinking(db.Model):
    venue = db.ReferenceProperty(Venue, required = True, collection_name = 'linked_things')
    thing = db.ReferenceProperty(Thing, required = True, collection_name = 'linked_venues')
    count = db.IntegerProperty(required = True, default = 1)
    created_at = db.DateTimeProperty(required = True, auto_now_add = True)
    updated_at = db.DateTimeProperty(required = True, auto_now = True)
    

class Affinity(db.Model):
    user = db.ReferenceProperty(User, required = True, collection_name = 'venues_with_affinity')
    venue = db.ReferenceProperty(Venue, required = True, collection_name = 'users_with_affinity')
    affinity = db.FloatProperty(required = True, default = 0)
    created_at = db.DateTimeProperty(required = True, auto_now_add = True)
    updated_at = db.DateTimeProperty(required = True, auto_now = True)