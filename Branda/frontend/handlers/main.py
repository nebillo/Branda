from base import *


class MainHandler(BaseHandler):
    def get(self):
        """Main Handler. Index is empty and redirect to graph

          :param name: self.
          :type name: self.
          :param state: Current state to be in.
          :type state: Self Object.
          :returns:  Void.
          :raises: Nothing
        """
        self.write("home")

