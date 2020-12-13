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
from flask import Flask, session
from flask_session import RedisSessionInterface, Session
from google.oauth2 import service_account
import os
import redis

APPURL = ""

if not os.getenv('GAE_ENV', '').startswith('standard'):
    credentials = service_account.Credentials.from_service_account_file('/mnt/c/users/steph/gae/mapartotheque.json')
    credential_path = "/mnt/c/users/steph/gae/mapartotheque.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    APPURL = "localhost:8080"
else:
    APPURL = "mapartotheque.net"

from .globalVar import *

sess = Session()
pool = redis.ConnectionPool(host=redis_host,
    port=redis_port,
    password=redis_password, max_connections=15)
redis_client = redis.Redis(connection_pool=pool)



IS_DEV = __name__ == '__main__'

from .mapartothequeClass import *
client = ndb.Client()

def create_app():
    app = Flask(__name__)
    app.secret_key = session_secret_key
    app.config['SECRET_KEY'] = session_secret_key
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis_client
    app.config.from_object(__name__)
    app.session_interface = RedisSessionInterface(redis_client, "sess_")
    sess.init_app(app)

    with app.app_context():
        from . import webapp
        from . import init
        from . import api
        from . import loginApi

        # Register Blueprints
        app.register_blueprint(webapp.bp)
        app.register_blueprint(init.bp)
        app.register_blueprint(api.bp)
        app.register_blueprint(loginApi.bp)

        return app





# [END gae_python37_app]
