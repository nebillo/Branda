import datetime
import logging

from libs import iso8601
from google.appengine.ext import db

from user import User
from thing import Thing, Page
from venue import Venue, Place, Event


# update the graph nodes with the facebook user data
class GraphUpdater:
    
    kPageType = "page"
    kPlaceType = "place"
    kEventType = "event"
    
    # initialize with a user
    def __init__(self, user):
        self.user = user;
    
    # update data and return whether nodes have been updated
    def updateNodes(self, info, likes, events, places):
        
        # coppie_venue = []
        venues_linkings = []
        # coppie_utente = []
        user_linkings = []
        
        # aggiorno le info utente non indicizzate
        self.updateUserBasicInfo(info)
        
        # aggiorno le info indicizzate
        self.updateReligionFromData(self.user, info)
        self.updatePoliticalFromData(self.user, info)
        
        # lista = merge degli eventi, pagine e posti
        # metto la lista in ordine cronologico
        stream = self.getStreamByMergingData(likes, events, places)
        
        # scorro ogni elemento della lista
        for element in stream:
            # pagina:
            if element.type == GraphUpdater.kPageType:
                # inizilizzo pagina
                page = self.pageFromData(element)
                # connetto utente a pagina ()
                page = self.connectUserToThing(self.user, page)
                ## coppie_utente += utente-pagina
            
            # venue:
            if element.type == GraphUpdater.kPlaceType or element.type == GraphUpdater.kEventType:
                # inizializzo venue
                if element.type == GraphUpdater.kPlaceType:
                    venue = self.placeFromData(element)
                else:
                    venue = self.eventFromData(element)
                # connetto utente a venue ()
                venue = self.connectUserToVenue(self.user, venue)
                
                # $cose_utente = cose collegate ad utente fino a quel momento
                user_things_until_now = self.user.linked_things()
                # $cose_venue = cose attive collegate a venue fino a quel momento
                venue_things_unitl_now = venue.linked_things()
                
                # per ogni $cosa in $cosa_utente:
                for thing in user_things_until_now:
                    # instauro o aumento legame tra venue e cosa
                    self.connectVenueToThing(venue, thing)
                    ## coppie_venue += $venue-$cosa
                
                # per ogni $cosa in $cose_venue:
                for thing in venue_things_unitl_now:
                    # instauro o aumento legame tra utente e cosa
                    self.connectUserToThing(self.user, thing)
                    ## coppie_utente += utente-pagina
                    
                # per ogni $cosa in $cose_utente non in $cose_venue:
                for thing in user_things_until_now:
                    if thing in venue_things_unitl_now:
                        continue
                    # incremento legame con $utente
                    self.increaseUserLinkingWithThing(self.user, thing)
                    ## coppie_utente += utente-pagina
        
        # coppie = []
        affinities = []
        
        # per ogni coppia in coppie_venue:
        for venue_thing in venues_linkings:
            users = self.users_linked_to_thing(venue_thing.thing())
            # per ogni utente collegato a coppia.cosa:
            for user in users:
                # coppie += coppia.venue-utente
                continue
            
        # per ogni coppia in coppie_utente:
        for thing in user_linkings:
            venues = self.venues_linked_to_thing(thing)
            # per ogni venue collegato a coppia.cosa:
            for venue in venues:
                # coppie += coppia.utente-venue
                continue
        
        # per ogni coppia in coppie:
        for affinity in affinities:
            # aggiorno affinita' tra coppia.venue e coppia.utente
            continue
                
        return len(affinities) > 0
        
        
    def updateUserBasicInfo(self, info):
        if "first_name" in info:
            self.user.first_name = info["first_name"]
        if "last_name" in info:
            self.user.last_name = info["last_name"]
        if "name" in info:
            self.user.name = info["name"]
        if "email" in info:
            self.user.email = info["email"]
        if "locale" in info:
            self.user.locale = info["locale"]
        if "gender" in info:
            self.user.gender = info["gender"]
        if "birthday" in info:
            birthday = info["birthday"]
            birthday = datetime.datetime.strptime(birthday, "%m/%d/%Y")
            self.user.birthday = birthday.date()
        return
    
    def updateReligionFromData(self, user, info):
        # imposto legame con vecchia info a zero
        # sovrascrivo info
        # inizializzi info
        # connetto utente a info ()
        ## coppie_utente += utente-info
        return
    
    def updatePoliticalFromData(self, user, info):
        # imposto legame con vecchia info a zero
        # sovrascrivo info
        # inizializzi info
        # connetto utente a info ()
        ## coppie_utente += utente-info
        return
    
    
    def getStreamByMergingData(self, likes, events, places):
        self.addTypeToObjects(likes, GraphUpdater.kPageType)
        self.addTypeToObjects(events, GraphUpdater.kEventType)
        self.addTypeToObjects(places, GraphUpdater.kPlaceType)
        merge = self.mergeOrderedArrays(likes, "created_time", places, "created_time")
        merge = self.mergeOrderedArrays(merge, "created_time", events, "start_time")
        return merge
    
    
    def addTypeToObjects(self, objects, value):
        for obj in objects:
            obj["type"] = value
            
    
    def mergeOrderedArrays(self, first_list, first_field, second_list, second_field):
        merge = []
        first_index = 0
        second_index = 0
        
        while first_index < len(first_list) and second_index < len(second_list):
            first = first_list[first_index]
            second = second_list[second_index]
            first_date = iso8601.parse_date(first[first_field])
            second_date = iso8601.parse_date(second[second_field])
            if first_date > second_date:
                merge.append(first)
                first_index += 1
            else:
                merge.append(second)
                second_index += 1
        
        merge.extend(first_list[first_index:])
        merge.extend(second_list[second_index:])
        
        return merge
        
    
    def pageFromData(self, data):
        """
        costruisce una istanza di Page a partire da un like di facebook
        o ritorna l'istanza salvata se esiste
        """
        # read page if exists
        query = Page.all()
        query.filter('facebook_id =', data["id"])
        page = query.get()
        if page:
            return page
            
        # create new page
        page = Page(name = data["name"], facebook_id = data["id"])
        if "category" in data:
            page.category = data["category"]
        if "picture" in data:
            page.picture_url = data["picture"]
        page.put()
        return page
    
    # nuova istanza di un luogo dai dati di fb
    def placeFromData(self, data):
        data = data["place"]
        coordinate = db.GeoPt(data["location"]["latitude"], data["location"]["longitude"])
        place = Place(name = data["name"], facebook_id = data["id"], location = coordinate)
        return place
    
    # nuova istanza di un evento dai dati di fb
    def eventFromData(self, data):
        venue = data["venue"]
        coordinate = db.GeoPt(venue["latitude"], venue["longitude"])
        
        event = Event(facebook_id = data["id"], location = coordinate, name = data["name"], venue_name = data["location"])
        
        event.country = venue["country"]
        event.address = self.postalAddressFromVenueData(venue)
        
        event.period = [iso8601.parse_date(data["start_time"]), iso8601.parse_date(data["end_time"])]
        
        if "description" in data:
            event.description = data["description"]
        if "picture" in data:
            event.picture_url = data["picture"]
            
        return event
    
    def postalAddressFromVenueData(self, data):
        address = ""
        
        if "street" in data:
            address += ", " + data["street"]
        if "city" in data:
            address += ", " + data["city"]
        if "zip" in data:
            address += ", " + data["zip"]
        if "state" in data:
            address += ", " + data["state"]
            
        if address[:2] == ", ":
            address = address[2:]
            
        address = db.PostalAddress(address)
        return address
    
    # connessione utente e cosa
    def connectUserToThing(self, usser, data):
        # cosa gia' connessa:
            # +1
        # cosa non connessa:
            # connetto
            # +3
            # aggiungo a cose di utente
        return None
    
    def increaseUserLinkingWithThing(self, user, thing):
        return
    
    # connessione utente a venue
    def connectUserToVenue(self, user, data):
        # venue non connesso:
            # aggiungo a venue di utente
        # aggiorno media eta'
        return None
    
    def connectVenueToThing(self, venue, thing):
        # se non esiste legame tra $venue e $cosa:
            # creo legame
        # incremento legame
        return None
    
    
    def users_linked_to_thing(self, thing):
        return []
    
    def venues_linked_to_thing(self, thing):
        return []
    

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