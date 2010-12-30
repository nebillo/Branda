from base import *
from libs.facebook import *
import json


class GraphHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        
        things_to_update = set([])
        if user.needsInfoUpdate():
            things_to_update.add('info')
        if user.needsLikesUpdate():
            things_to_update.add('likes')
        if user.needsEventsUpdate():
            things_to_update.add('events')
        if user.needsPlacesUpdate():
            things_to_update.add('places')
        
        if len(things_to_update) > 0:
            self.render("graph-update.html", options = options, things_to_update = things_to_update, title = "Updating")
        else:
            self.render("graph.html", options = options, title = "Grafo")
    
    @tornado.web.authenticated    
    def post(self):
        self.write("update")
        if self.get_argument("info"):
            info = self.get_argument("info")
            info = json.loads(info)
            self.write("<br>received info: " + str(len(info)))
        if self.get_argument("likes"):
            likes = self.get_argument("likes")
            likes = json.loads(likes)
            self.write("<br>received likes: " + str(len(likes)))
        if self.get_argument("events"):
            events = self.get_argument("events")
            events = json.loads(events)
            self.write("<br>received events: " + str(len(events)))
        if self.get_argument("places"):
            places = self.get_argument("places")
            places = json.loads(places)
            self.write("<br>received places: " + str(len(places)))
            