import datetime


# update the graph nodes with the facebook user data
class GraphUpdater:
    
    # initialize with a user
    def __init__(self, user):
        self.user = user;
    
    # update data and return whether nodes have been updated
    def updateNodes(self, info, likes, events, places):
        return False


# read the graph data suggested for a user
class GraphReader:
    
    # initialize with a user
    def __init__(self, user):
        self.user = user;
    
    # set query parameters
    def setQueryParameters(self, latitude, longitude, date, exclude_mine = False):
        self.latitude = latitude
        self.longitude = longitude
        self.date = date
        self.exclude_mine = exclude_mine
        self.cursor = None
        
    # set query cusors
    def setQueryCursor(cursor):
        self.cursor = cursor
    
    # fetch data
    def fetchData(self, limit = 20, offset = 0):
        return []