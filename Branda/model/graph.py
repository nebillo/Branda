import datetime


# update the graph nodes with the facebook user data
class GraphUpdater:
    
    # initialize with a user
    def __init__(self, user):
        self.user = user;
    
    # update data and return whether nodes have been updated
    def updateNodes(self, info, likes, events, places):
        
        # coppie_venue = []
        # coppie_utente = []
        
        # aggiorno le info utente non indicizzate
        
        
        # per ogni info utente indicizzata (religion, political):
            # imposto legame con vecchia info a zero
            # sovrascrivo info
            # inizializzi info
            # connetto utente a info ()
            ## coppie_utente += utente-info
        
        # lista = merge degli eventi, pagine e posti
        # metto la lista in ordine cronologico
                
        # scorro ogni elemento della lista
            # pagina:
                # inizilizzo pagina
                # connetto utente a pagina ()
                ## coppie_utente += utente-pagina
            # venue:
                # $plaven = inzializzo venue
                # connetto utente a venue ()
                # $cose_utente = cose collegate ad utente fino a quel momento
                # $cose_venue = cose attive collegate a venue fino a quel momento
                
                # per ogni $cosa in $cosa_utente:
                    # se non esiste legame tra $venue e $cosa:
                        # creo legame
                    # incremento legame
                    ## coppie_venue += $venue-$cosa
                # per ogni $cosa in $cose_venue:
                    # se non esiste legame tra $utente e $cosa:
                        # creo legame
                    # incremento legame
                    ## coppie_utente += utente-pagina
                # per ogni $cosa in $cose_utente non in $cose_venue:
                    # incremento legame con $utente
                    ## coppie_utente += utente-pagina
        
        # coppie = []
        # per ogni coppia in coppie_venue:
            # per ogni utente collegato a coppia.cosa:
                # coppie += coppia.venue-utente
        # per ogni coppia in coppie_utente:
            # per ogni venue collegato a coppia.cosa:
                # coppie += coppia.utente-venue
        
        # per ogni coppia in coppie:
            # aggiorno affinita' tra coppia.venue e coppia.utente
                
        return False
        
        
    # connessione utente a info ():
        # info gia' connessa:
            # +1
        # info non connessa:
            # connetto
            # +3
            # aggiungo a pagine di utente
        
    # connessione utente a pagina ():
        # pagina gia' connessa:
            # +1
        # pagina non connessa:
            # connetto
            # +3
            # aggiungo a pagine di utente
        
    # connessione utente a venue ():
        # venue non connesso:
            # aggiungo a venue di utente
        # aggiorno media eta'
        

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