from google.appengine.ext import db
from google.appengine.ext.db import polymodel


class Thing(polymodel.PolyModel):
    facebook_id = db.StringProperty(required = True)
    created_at = db.DateTimeProperty(required = True, auto_now_add = True)


class Page(Thing):
    name = db.StringProperty(required = True)
    category = db.StringProperty()
    picture_url = db.LinkProperty()


class Political(Thing):
    name = db.StringProperty(required = True)


class Religion(Thing):
    name = db.StringProperty(required = True)
