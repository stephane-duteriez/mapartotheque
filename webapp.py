from flask import Flask, render_template, Blueprint 
from mapartothequeClass import *

client = ndb.Client()
bp = Blueprint('webapp', __name__, url_prefix='/')

@bp.route('/')
def main():
    with client.context() as context:
        b_rythmes = Rythm.query()
        lTunesForTemplate = {}
        for rythme in b_rythmes:
            lTunesForTemplate[rythme.id_rythme] = RythmForDisplay(rythme)
        b_tunes =  Tune.query().order(Tune.titre)
        for tune in b_tunes:
            lTunesForTemplate[tune.id_rythme].add_tune(tune)
        return render_template('listTunes.html', list_tunes = lTunesForTemplate)

@bp.route('/home/sessions')
def listSessions():
    with client.context() as context:
        lRythmes = Rythm.query()
        lSessionsForTemplate = {}
        for rythme in lRythmes:
            lSessionsForTemplate[rythme.id_rythme] = RythmForDisplay(rythme)
        lSessions =  Session.query().order(Session.name_session)
        for session in lSessions:
            lSessionsForTemplate[session.id_rythme].add_tune(session)
        return render_template('listSessions.html', listSessions = lSessionsForTemplate)

@bp.route('/home/view/<int:idTune>')
def ViewTune(idTune):
    with client.context() as context:
        b_tunes = Tune.query(Tune.id_tune==int(idTune))
        if (b_tunes) :
            tune = b_tunes.get()
            return render_template('show_tune.html', tune=tune, list_siblings=[])

@bp.route('/home/viewSession/<int:idSession>')
def ViewSession(idSession):
    with client.context() as context:
        sessions = Session.query(Session.id_session==int(idSession))
        if (sessions) :
            session = sessions.get()
            return render_template('show_session.html', session=session)
        else :
            return "Session non trouvée : " + idSession


