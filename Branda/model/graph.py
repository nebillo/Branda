import datetime
import logging
import math

from libs import iso8601
from google.appengine.ext import db

from user import User
from thing import Thing, Page
from venue import Venue, Place, Event
from affinity import UserLinking, VenueLinking, Affinity


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
                # connetto utente a pagina
                page = self.connectUserToThing(page, UserLinking.kActiveLinkingMinimumCount)
                # e aggiungo all'elenco delle cose proprie
                self.addThingToUserList(page)
                ## coppie_utente += utente-pagina
            
            # venue:
            if element.type == GraphUpdater.kPlaceType or element.type == GraphUpdater.kEventType:
                # inizializzo venue
                if element.type == GraphUpdater.kPlaceType:
                    venue = self.placeFromData(element)
                else:
                    venue = self.eventFromData(element)
                    # se questo evento e' gia' associato all'utente devo evitare di rielaborlo
                # connetto utente a venue ()
                venue = self.addVenueToUserList(self.user, venue)
                
                # active things connected to user until now
                user_things_until_now = self.getUserActiveThings()
                # active things connected to venue until now
                venue_things_unitl_now = self.getVenueActiveThings(venue)
                
                for thing in user_things_until_now:
                    # instauro o aumento legame tra venue e cosa
                    self.connectVenueToThing(venue, thing)
                    ## coppie_venue += $venue-$cosa
                
                for thing in venue_things_unitl_now:
                    # instauro o aumento legame tra utente e cosa
                    self.connectUserToThing(thing)
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
    
    
    def placeFromData(self, data):
        """
        costruisce una istanza di Place a partire da un checkin di facebook
        o ritorna l'istanza salvata se esiste
        """
        # read place if exists
        data = data["place"]
        query = Place.all()
        query.filter('facebook_id =', data["id"])
        place = query.get()
        if place:
            return place
            
        # create new place
        coordinate = db.GeoPt(data["location"]["latitude"], data["location"]["longitude"])
        place = Place(name = data["name"], facebook_id = data["id"], location = coordinate)
        place.put()
        return place
    
    
    def eventFromData(self, data):
        """
        costruisce una istanza di Event a partire da un evento di facebook
        o ritorna l'istanza salvata se esiste
        """
        # read event if exists
        query = Event.all()
        query.filter('facebook_id =', data["id"])
        event = query.get()
        if event:
            return event
            
        # create new event
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
        event.put()
        return event
    
    
    def postalAddressFromVenueData(self, data):
        """
        costruisce una PostalAddress concatenando le varie informazioni presenti in data
        esempio: via topo 69/b, zelarino, 30174, VE
        """
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
    
    
    def connectUserToThing(self, thing, increment = 1):
        """
        crea un legame tra user e thing
        o incrementa il legame se esiste
        """
        query = UserLinking.all()
        query.filter('user =', self.user)
        query.filter('thing =', thing)
        linking = query.get()
        
        if linking:
            linking.count += increment
        else:
            linking = UserLinking(user = self.user, thing = thing, count = increment)
            
        if linking.count >= UserLinking.kActiveLinkingMinimumCount:
            linking.is_active = True
        
        linking.put()
        return linking
    
    
    def addThingToUserList(self, thing):
        """
        thing viene aggiunta alle cose dell'utente
        nel caso non sia gia' presente
        """
        things = self.user.things
        for existing_thing in things:
            if existing_thing == thing.key():
                # found
                return things
        # not found, add
        things.append(thing.key())
        self.user.put()
        return things
    
    
    def addVenueToUserList(self, venue):
        """
        venue viene aggiunta alle venue dell'utente
        nel caso non sia gia' presente
        inoltre aggiorno la media dell'eta della venue
        """
        venues = self.user.venues
        for existing_venue in venues:
            if existing_venue == venue.key():
                # found
                return venues
        # not found, add
        venues.append(venue.key())
        self.user.put()
        
        # aggiorno media eta'
        venue.updateTargetAgeWithUser(self.user)
        
        return venues
    
    
    def connectVenueToThing(self, venue, thing):
        """
        crea un legame tra venue e thing
        o incrementa il legame se esiste
        """
        query = VenueLinking.all()
        query.filter('venue =', venue)
        query.filter('thing =', thing)
        linking = query.get()
        
        if linking:
            # cosa gia' connessa
            linking.count += 1
        else:
            # cosa non connessa
            # connetto
            linking = VenueLinking(venue = venue, thing = thing, count = 1)
        
        if linking.count >= VenueLinking.kActiveLinkingMinimumCount:
            linking.is_active = True
            
        linking.put()
        return linking
    
    
    def getUserActiveThings(self, days = None, since_date = None, limit = 10):
        """
        retrieve the active things linked to the user
        not older than a minimum period
        """
        # get the date limit
        if not days:
            days = UserLinking.kActiveLinkingMaximumDays
        if not since_date:
            since_date = datetime.datetime.now()
        minimum_date = since_date - datetime.timedelta(days = days)
    
        # get the active linkings
        query = db.GqlQuery('SELECT * FROM UserLinking WHERE user = :1 AND updated_at >= :2 AND is_active = :3 order by updated_at, count desc', 
                            self.user.key(), minimum_date, True)
        linkings = query.fetch(limit)
    
        # get the things
        things = [linking.thing.key() for linking in linkings]
        return things
    
    
    def getVenueActiveThings(self, venue, days = None, since_date = None, limit = 10):
        """
        retrieve the things linked to the venue
        with a minimum linking count
        """
        # get the date limit
        if not days:
            days = VenueLinking.kActiveLinkingMaximumDays
        if not since_date:
            since_date = datetime.datetime.now()
        minimum_date = since_date - datetime.timedelta(days = days)
    
        # get the active linkings
        query = db.GqlQuery('SELECT * FROM VenueLinking WHERE venue = :1 AND updated_at >= :2 AND is_active = :3 order by updated_at, count desc', 
                            venue.key(), minimum_date, True)
        linkings = query.fetch(limit)
    
        # get the things
        things = [linking.thing.key() for linking in linkings]
        return things
    
    
    def users_linked_to_thing(self, thing):
        return []
    
    
    def venues_linked_to_thing(self, thing):
        return []
    
    
    def updateAffinity(self, user, venue):
        """
        update affinity from user and venue
        based on linked things in common
        """
        # get user-thing's linkings
        user_linkings = user.linkings.fetch(99999)
        # get venue-thing's linkings
        venue_linkings = venue.linkings.fetch(99999)
        
        affinity_value = 0.0
        for u_linking in user_linkings:
            # search u_linking.thing in each venue_linking.thing
            for v_linking in venue_linkings:
                if u_linking.thing.key() == v_linking.thing.key():
                    affinity_value += self.calculateAffinity(u_linking.count, v_linking.count)
                    venue_linkings.remove(v_linking)
                    break
                
        
        # search for existing affinity between user and venue
        query = Affinity.all()
        query.filter('user =', user)
        query.filter('venue =', venue)
        affinity = query.get()
        if not affinity:
            affinity = Affinity(user = user, venue = venue)
            
        # save affinity
        affinity.value = affinity_value
        affinity.put()
        return affinity
    
    
    def calculateAffinity(self, count_a, count_b):
        return - math.fabs(count_a - count_b) / max(math.fabs(count_a), math.fabs(count_b)) + 1
        

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