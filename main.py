# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, render_template
from mapartothequeClass import *

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

IS_DEV = __name__ == '__main__'

client = ndb.Client()

import webapp
app.register_blueprint(webapp.bp)

@app.route('/initdatabase')
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

@app.route('/addmoretune')
def AddMoreTune():
    with client.context() as context:
        b_tune = Tune()
        b_tune.titre = "default"
        b_tune.id_tune = 1
        b_tune.id_rythme = 1
        b_tune.image_file = "0qtibeotdwt.png"
        b_tune.id_youtubelink = "http://youtu.be/0r3cEKZiLmg"
        b_tune.put()

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
