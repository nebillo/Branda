from google.appengine.ext import db

import datetime

from user import User
from venue import Venue
from thing import Thing


class UserLinking(db.Model):
    
    kActiveLinkingMinimumCount = 3
    
    user = db.ReferenceProperty(User, required = True, collection_name = 'linkings')
    thing = db.ReferenceProperty(Thing, required = True, collection_name = 'linkings_with_user')
    count = db.IntegerProperty(required = True, default = 1)
    is_active = db.BooleanProperty(required = True, default = False)
    created_at = db.DateTimeProperty(required = True, auto_now_add = True)
    updated_at = db.DateTimeProperty(required = True, auto_now = True)  


class VenueLinking(db.Model):
    
    kActiveLinkingMinimumCount = 3
    kActiveLinkingMaximumDays = 45
    
    venue = db.ReferenceProperty(Venue, required = True, collection_name = 'linkings')
    thing = db.ReferenceProperty(Thing, required = True, collection_name = 'linkings_with_venue')
    count = db.IntegerProperty(required = True, default = 1)
    is_active = db.BooleanProperty(required = True, default = False)
    created_at = db.DateTimeProperty(required = True, auto_now_add = True)
    updated_at = db.DateTimeProperty(required = True, auto_now = True)


class Affinity(db.Model):
    user = db.ReferenceProperty(User, required = True, collection_name = 'affinities')
    venue = db.ReferenceProperty(Venue, required = True, collection_name = 'affinities')
    affinity = db.FloatProperty(required = True, default = 0)
    created_at = db.DateTimeProperty(required = True, auto_now_add = True)
    updated_at = db.DateTimeProperty(required = True, auto_now = True)
