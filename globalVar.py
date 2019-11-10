import redis
import os
import json

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_password = os.environ.get('REDIS_PASSWORD', None)
redis_client = redis.StrictRedis(host=redis_host,
    port=redis_port,
    password=redis_password,
    health_check_interval=30)
session_secret_key = os.environ.get("SESSION_SECRET_KEY", None)