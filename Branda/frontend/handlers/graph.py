from base import *
from libs.facebook import *
from django.utils import simplejson as json
from tornado.escape import *
import datetime


class GraphHandler(BaseHandler):
    
    # graph
    @tornado.web.authenticated
    def get(self):
        if self.get_current_user().neverUpdated():
            self.render("graph-update.html", options = options, title = "Updating")
        else:
            self.render("graph.html", options = options, title = "Graph")
    

class GraphDataHandler(BaseHandler):
    
    # update user data
    @tornado.web.authenticated
    def post(self):
        self.write("update data")
        user = self.get_current_user()
        
        if self.get_argument("info"):
            info = self.get_argument("info")
            info = url_unescape(info)
            info = json.loads(info)
            self.write("<br>received info: " + str(len(info)))
        if self.get_argument("likes"):
            likes = self.get_argument("likes")
            likes = url_unescape(likes)
            likes = json.loads(likes)
            self.write("<br>received likes: " + str(len(likes)))
        if self.get_argument("events"):
            events = self.get_argument("events")
            events = url_unescape(events)
            events = json.loads(events)
            self.write("<br>received events: " + str(len(events)))
        if self.get_argument("places"):
            places = self.get_argument("places")
            places = url_unescape(places)
            places = json.loads(places)
            self.write("<br>received places: " + str(len(places)))
        
        user.updated_at = datetime.datetime.now()
        user.put()
        
    
    # get graph data  
    @tornado.web.authenticated
    def get(self):
        self.write("read data")
    