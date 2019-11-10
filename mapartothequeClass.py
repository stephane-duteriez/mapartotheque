from google.cloud import ndb
from globalVar import *

class Rythm(ndb.Model):
    id_rythme = ndb.IntegerProperty()
    nom_rythme = ndb.StringProperty()
    lastChanged = ndb.DateTimeProperty(auto_now = True)
    @classmethod
    def getAll(cls):
        cache_rythmes = redis_client.get("rythmes")
        if cache_rythmes :
            b_rythmes = json.loads(cache_rythmes)
        else :
            b_rythmes = cls.query()
            redis_client.set("rythmes", json.dumps(b_rythmes))
        return b_rythmes

class Tune(ndb.Model):
    id_tune = ndb.IntegerProperty()
    ref_tune = ndb.StringProperty()
    titre = ndb.StringProperty()  # name of the tune
    auteur = ndb.StringProperty()
    youtubelink = ndb.StringProperty()
    text_ly = ndb.TextProperty()
    chords = ndb.TextProperty()
    image_file = ndb.StringProperty()
    pdf_file = ndb.StringProperty()
    id_rythme = ndb.IntegerProperty()
    lastChanged = ndb.DateTimeProperty(auto_now = True)
    @classmethod
    def getAll(cls):
        cache_tunes = redis_client.get("tunes")
        if cache_tunes :
            b_tunes = json.loads(cache_tunes)
        else :
            b_tunes = cls.query()
            redis_client.set("tunes", json.dumps(b_tunes))
        return b_tunes

class Session(ndb.Model):
    name_session = ndb.StringProperty()
    image_session=ndb.StringProperty()
    pdf_session = ndb.StringProperty()
    id_rythme = ndb.IntegerProperty()
    id_session = ndb.IntegerProperty()
    lastChanged = ndb.DateTimeProperty(auto_now = True)
     
class Tune_in_session(ndb.Model):
    id_tune = ndb.IntegerProperty()
    id_session = ndb.IntegerProperty()
    pos = ndb.IntegerProperty()
    lastChanged = ndb.DateTimeProperty(auto_now = True)

class RythmForDisplay():
    def __init__(self, rythme):
        self.rythme = rythme
        self.listTunes = []
    def add_tune(self, tune):
        self.listTunes.append(tune)

class User():
    sqrlId =  ndb.StringProperty()
    lastChanged = ndb.DateTimeProperty(auto_now = True)