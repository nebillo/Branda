"""
.. module:: Graph Handler
   :platform: Tornado Web Framework
   :synopsis: Graph Handler

.. moduleauthor:: Branda Developing Team <dev@branda.something>


"""

from base import *
from libs.facebook import *
from tornado.escape import *
import datetime
import logging
from model.graph import GraphUpdater, GraphReader


class GraphHandler(BaseHandler):
    
    # graph
    @tornado.web.authenticated
    def get(self):
        if self.get_current_user().neverUpdated():
            self.render("graph-update.html", options = options, title = "Updating")
        else:
            self.render("graph.html", options = options, title = "Graph")
    

class GraphDataHandler(BaseHandler):
    
    def getFacebookData(self, key, default = None):
        """Get Facebok Data. Decode Json and return data
              :param name: self.
              :type name: self.
              :param state: Current state to be in.
              :type state: Self Object.
              :param name: key.
              :type name: key.
              :param state: not null.
              :type state: boh.
              :returns:  data.
              :raises: Nothing
        """
        
        string = self.get_argument(key)
        if not string:
            return default
        
        data = json_decode(string)
        if not data:
            return default
            
        return data
        
    @tornado.web.authenticated
    def post(self):
      
        """Get data from Facebook and update user graph. It sets date of expiration data.

          :param name: self.
          :type name: self.
          :param state: Current state to be in.
          :type state: Self Object.
          :returns:  data.
          :raises: HTTPError(400).

        """
        user = self.get_current_user()
        
        # read parameters
        info = self.getFacebookData("info")
        if not info:
          raise tornado.web.HTTPError(400)
          
        likes = self.getFacebookData("likes", [])
        events = self.getFacebookData("events", [])
        places = self.getFacebookData("places", [])
        
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
      
        """Geolocate the user and fetch data from graph?.

            :param name: self.
            :type name: self.
            :param state: Current state to be in.
            :type state: Self Object.
            :returns:  data.
            :raises: HTTPError(400).

        """
        user = self.get_current_user()
        
        # read parameters
        latitude = self.get_argument("latitude")
        if not latitude:
            raise tornado.web.HTTPError(400)
            latitude = float(latitude)
            
        longitude = self.get_argument("longitude")
        if not latitude:
            raise tornado.web.HTTPError(400)
        longitude = float(longitude)
        
        date = self.get_argument("date")
        if not date:
            raise tornado.web.HTTPError(400)
        date = float(date)
        date = datetime.datetime.fromtimestamp(date)
        
        logging.info("user: %s, fetch data around: %f,%f date: %s", user.facebook_id, float(latitude), float(longitude), str(date))
        
        reader = GraphReader(user)
        reader.setQueryParameters(latitude = latitude, longitude = longitude, date = date)
        data = reader.fetchData()
        
        self.write(json_encode({ "data": data }))
    