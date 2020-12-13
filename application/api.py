from flask import Flask, render_template, Blueprint, jsonify, request
from .mapartothequeClass import Tune, Session, Tune_in_session, Rythm, RythmForDisplay, User
import json
from . import client, redis_client

bp = Blueprint('api', __name__, url_prefix='/')

def cleanCacheTunes():
    redis_client.delete("main")
    redis_client.delete("listTunes")

def cleanCacheSessions():
    redis_client.delete("sessions")
    redis_client.delete("listSessions")

@bp.route('/api/apiTunes/cleanCache')
def cleanCache():
    cleanCacheSessions()
    cleanCacheTunes()
    return "Ok"

@bp.route('/api/apiTunes/', methods=['GET'])
def getTune():
    result = redis_client.get("listTunes")
    if not result:   
        with client.context() as context:
            b_tunes=Tune.query().order(Tune.titre)
            listTune = []
            for tune in b_tunes:
                listTune.append(tune.to_dict())
            result = json.dumps(listTune, default=str)
            redis_client.set("listTunes", result)
    return jsonify(json.loads(result))

@bp.route('/api/apiTunes/<int:idTune>', methods=['PUT'])
def putTune(idTune):
    with client.context() as context:
        dictionary = request.json
        tune = Tune.query(Tune.id_tune==int(idTune)).get()
        if not tune :
            tune = Tune()
        dictionary.pop('Rythme', None)
        tune.populate(**dictionary)
        tune.put()
        return ""
    
@bp.route('/api/apiTunes/', methods=['POST'])
def postTune():
    cleanCacheTunes()
    with client.context() as context:
        dictionary = request.json
        tune = Tune()
        dictionary.pop('Rythme', None)
        tune.populate(**dictionary)
        new_id = Tune().query().order(-Tune.id_tune).get().id_tune + 1
        tune.id_tune=new_id
        tune.put()
        return jsonify(tune.to_dict())

@bp.route('/api/apiTunes/<int:idTune>', methods=['DELETE'])
def deleteTune(idTune):
    cleanCacheTunes()
    with client.context() as context:
        tune = Tune.query(Tune.id_tune==int(idTune)).get()
        if tune:
            tune.key.delete()
        return ""


@bp.route('/api/apiSessions/', methods=['GET'])
def getSession():
    with client.context() as context:
        b_session=Session.query().order(Session.name_session)
        result = []
        for session in b_session:
            result.append(session.to_dict())
        return jsonify(result)

@bp.route('/api/apiSessions/<int:idSession>', methods=['PUT'])
def putSession(idSession):
    with client.context() as context:
        dictionary = request.json
        session = Session().query(Session.id_session==int(idSession)).get()
        if not session :
            session = Session()
        dictionary.pop( 'Rythme', None)
        session.populate(**dictionary)
        session.put()
        return ""

@bp.route('/api/apiSessions/', methods=['POST'])
def postSession():
    cleanCacheSessions()
    with client.context() as context:
        dictionary = request.json
        session = Session()
        dictionary.pop('Rythme', None)
        session.populate(**dictionary)
        new_id = Session().query().order(-Session.id_session).get().id_session + 1
        session.id_session = new_id
        session.put()
        return ""

@bp.route('/api/apiSessions/<int:idSession>', methods=['DELETE'])
def deleteSession(idSession):
    cleanCacheSessions()
    with client.context() as context:
        session = Session.query(Session.id_session==int(idSession)).get()
        if session:
            session.key.delete()
        return ""

@bp.route('/api/apiRythmes/', methods=['GET'])
def getRythme():
    with client.context() as context:
        b_rythme=Rythm.query()
        result = []
        for rythme in b_rythme:
            result.append(rythme.to_dict())
        return jsonify(result)

@bp.route('/api/apiRythmes/', methods=['POST'])
def postRythme():
    with client.context() as context:
        dictionary = request.json
        rythme = Rythm()
        rythme.populate(**dictionary)
        rythme.put()
        return ""
        
@bp.route('/api/apiTunesInSessions/', methods=['GET'])
def getTunesInSession():
    with client.context() as context:
        b_tunesInSessions=Tune_in_session.query()
        result = []
        for tunesInSession in b_tunesInSessions:
            result.append(tunesInSession.to_dict())
        return jsonify(result)

@bp.route('/api/apiTunesInSessions/', methods=['POST'])
def postTunesInSession():
    cleanCacheSessions()
    with client.context() as context:
        dictionary = request.json
        tis = Tune_in_session()
        tis.populate(**dictionary)
        tis.put()
        return ""

@bp.route('/api/apiTunesInSessions/<int:idSession>', methods=['DELETE'])
def deleteTuneInSession(idSession):
    cleanCacheSessions()
    with client.context() as context:
        l_tis = Tune_in_session.query(Tune_in_session.id_session==int(idSession))
        if l_tis:
            for tis in l_tis:
                tis.key.delete()
        return ""