from flask import Flask, render_template, Blueprint 
from mapartothequeClass import *

client = ndb.Client()
bp = Blueprint('api', __name__, url_prefix='/')


class ApiTunes(webapp2.RequestHandler):
    def get(self, id_tune):
        b_tunes=Tune.query().order(Tune.titre)
        result = []
        for tune in b_tunes:
            result.append(tune.to_dict())
        self.response.headers['Content-Type'] = 'application/json'  
        self.response.out.write(json.dumps(result))

    def put(self, id_tune):
        dictionary = json.loads(self.request.body)
        tune = Tune.query(Tune.id_tune==int(id_tune)).get()
        dictionary.pop('Rythme', None)
        tune.populate(**dictionary)
        delete_index_pages(tune.id_rythme, False);
        tune.put()
    
    def post(self, id_tune):
        dictionary = json.loads(self.request.body)
        tune = Tune()
        dictionary.pop('Rythme', None)
        tune.populate(**dictionary)
        new_id = Tune().query().order(-Tune.id_tune).get().id_tune + 1
        tune.id_tune=new_id
        tune.put()
        self.response.headers['Content-Type'] = 'application/json'
        delete_index_pages(tune.id_rythme, False)
        self.response.out.write(json.dumps(tune.to_dict()))

    def delete(self, id_tune):
        tune = Tune.query(Tune.id_tune==int(id_tune)).get()
        if tune:
            tune.key.delete()

class ApiSessions(webapp2.RequestHandler):
    def get(self, id_session):
        b_session=Session.query().order(Session.name_session)
        result = []
        for session in b_session:
            result.append(session.to_dict())
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(result))

    def put(self, id_session):
        dictionary = json.loads(self.request.body)
        session = Session().query(Session.id_session==int(id_session)).get()
        dictionary.pop( 'Rythme', None)
        session.populate(**dictionary)
        delete_index_pages(session.id_rythme, True)
        session.put()

    def post(self, id_session):
        dictionary = json.loads(self.request.body)
        session = Session()
        dictionary.pop('Rythme', None)
        session.populate(**dictionary)
        new_id = Session().query().order(-Session.id_session).get().id_session + 1
        session.id_session = new_id
        session.put()
        self.response.headers['Content-Type'] = 'application/json'
        delete_index_pages(session.id_rythme, True);
        self.response.out.write(json.dumps(session.to_dict()))

    def delete(self, id_session):
        session = Session.query(Session.id_session==int(id_session)).get()
        if session:
            session.key.delete()

class ApiRythmes(webapp2.RequestHandler):
    def get(self):
        b_rythme=Rythm.query()
        result = []
        for rythme in b_rythme:
            result.append(rythme.to_dict())
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(result))
        
class ApiTunesInSessions(webapp2.RequestHandler):
    def get(self, id_session):
        b_tunesInSessions=Tune_in_session.query()
        result = []
        for tunesInSession in b_tunesInSessions:
            result.append(tunesInSession.to_dict())
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(result))

    def post(self, id_session):
        dictionary = json.loads(self.request.body)
        tis = Tune_in_session()
        tis.populate(**dictionary)
        tis.put()

    def delete(self, id_session):
        l_tis = Tune_in_session.query(Tune_in_session.id_session==int(id_session))
        for tis in l_tis:
           tis.key.delete()