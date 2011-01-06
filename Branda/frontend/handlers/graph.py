from base import *
from libs.facebook import *
from django.utils import simplejson as json


class GraphHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.get_current_user().needsUpdate():
            self.render("graph-update.html", options = options, title = "Updating")
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
            