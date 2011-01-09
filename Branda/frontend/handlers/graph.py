from base import *
from libs.facebook import *
from tornado.escape import *
import datetime
import logging
from model.graph import GraphUpdater


class GraphHandler(BaseHandler):
    
    # graph
    @tornado.web.authenticated
    def get(self):
        if self.get_current_user().neverUpdated():
            self.render("graph-update.html", options = options, title = "Updating")
        else:
            self.render("graph.html", options = options, title = "Graph")
    

class GraphDataHandler(BaseHandler):
    
    def getFacebookData(self, key):
        if not self.get_argument(key):
            return None
        
        string = self.get_argument(key)
        if not string:
            return None
        
        data = json_decode(string)
        if not data:
            return None
            
        return data
        
    # update user data
    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        
        # read parameters
        info = self.getFacebookData("info")
        if not info:
            raise tornado.web.HTTPError(400)
        
        likes = self.getFacebookData("likes")
        if not likes:
            raise tornado.web.HTTPError(400)
        
        events = self.getFacebookData("events")
        if not events:
            raise tornado.web.HTTPError(400)
        
        places = self.getFacebookData("places")
        if not places:
            raise tornado.web.HTTPError(400)
        
        logging.info("user: %s, received info: %d, likes: %d, events: %d, places: %d", user.facebook_id, len(info), len(likes), len(events), len(places))
        
        updater = GraphUpdater(user)
        nodes_updated = updater.updateNodes(info = info, likes = likes, places = places, events = events)
        
        self.write(json_encode({ "nodes_updated": nodes_updated }))
        
        if self.get_argument("until_date"):
            user.updated_at = datetime.datetime.fromtimestamp(float(self.get_argument("until_date")))
        else:
            user.updated_at = datetime.datetime.now()
        user.put()
        
    
    # get graph data  
    @tornado.web.authenticated
    def get(self):
        self.write("read data")
    