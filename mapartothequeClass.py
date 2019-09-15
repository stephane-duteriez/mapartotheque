from google.appengine.ext import ndb

class Rythm(ndb.Model):
    id_rythme = ndb.IntegerProperty()
    nom_rythme = ndb.StringProperty()
    lastChanged = ndb.DateTimeProperty(auto_now = True)

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