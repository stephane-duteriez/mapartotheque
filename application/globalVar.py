import os
from flask_session import Session

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_password = os.environ.get('REDIS_PASSWORD', None)
session_secret_key = os.environ.get("SESSION_SECRET_KEY", None)
SESSION_TYPE = 'redis'