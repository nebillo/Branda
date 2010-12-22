from base import *
from libs.facebook import *


class GraphHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        
        if user.isFirstLaunch():
            # get info from facebook
            graph_api = GraphAPI(user.facebook_access_token)
            user_info = graph_api.get_object("/me")
            if not user_info:
                raise tornado.web.HTTPError(400)
            # update user with info
            user.updateWithDictionary(user_info)
            
        self.render(
            "graph.html", 
            options = options, 
            title = "Grafo",
            needs_to_update_info = user.needsToUpdateInfo())