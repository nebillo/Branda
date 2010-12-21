from base import *


class MainHandler(BaseHandler):
    def get(self):
        # now index is empty, redirect to graph
        self.redirect("/graph")