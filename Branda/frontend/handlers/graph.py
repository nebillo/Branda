from base import *


class GraphHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("graph.html", options = options, title = "Grafo")