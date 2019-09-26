from flask import Flask, render_template, Blueprint 
from mapartothequeClass import *

client = ndb.Client()
bp = Blueprint('init', __name__, url_prefix='/')

@bp.route('/initdatabase')
def InitLocal():
    with client.context() as context:
        b_rythme = Rythm()
        b_rythme.nom_rythme = "test"
        b_rythme.id_rythme= 1
        b_rythme.put()
        b_tune = Tune()
        b_tune.titre = "default"
        b_tune.id_tune = 1
        b_tune.id_rythme = 1
        b_tune.image_file = "0qtibeotdwt.png"
        b_tune.id_youtubelink = "http://youtu.be/0r3cEKZiLmg"
        b_tune.put()
        b_session = Session()
        b_session.name_session = "test"
        b_session.id_session = 1
        b_session.id_rythme = 1
        b_session.put()
        b_tuneInSession = Tune_in_session()
        b_tuneInSession.id_session = b_session.id_session
        b_tuneInSession.id_tune = b_tune.id_tune
        b_tuneInSession.pos = 0
        b_tuneInSession.put()

@bp.route('/addmoretune')
def AddMoreTune():
    with client.context() as context:
        b_tune = Tune()
        b_tune.titre = "default"
        b_tune.id_tune = 1
        b_tune.id_rythme = 1
        b_tune.image_file = "0qtibeotdwt.png"
        b_tune.id_youtubelink = "http://youtu.be/0r3cEKZiLmg"
        b_tune.put()