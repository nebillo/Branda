from base import *
from libs.facebook import *
from tornado.escape import *
import datetime
import logging


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
        updated = False
        
        if self.get_argument("info"):
            info = self.get_argument("info")
            info = json_decode(info)
            logging.info("received info: " + str(len(info)))
            updated = True
        if self.get_argument("likes"):
            likes = self.get_argument("likes")
            likes = json_decode(likes)
            logging.info("received likes: " + str(len(likes)))
            updated = True
        if self.get_argument("events"):
            events = self.get_argument("events")
            events = json_decode(events)
            logging.info("received events: " + str(len(events)))
            updated = True
        if self.get_argument("places"):
            places = self.get_argument("places")
            places = json_decode(places)
            logging.info("received places: " + str(len(places)))
            updated = True
        
        self.write(json_encode({"updated": updated}))
        
        if self.get_argument("until_date"):
            user.updated_at = datetime.datetime.fromtimestamp(float(self.get_argument("until_date")))
        else:
            user.updated_at = datetime.datetime.now()
        user.put()
        
    
    # get graph data  
    @tornado.web.authenticated
    def get(self):
        self.write("read data")
    