from base import *
from libs.facebook import *


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