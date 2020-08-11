import os
import secrets

FLASK_APP = 'myapp'
SESSION_TYPE = 'filesystem'
SECRETE_KEY = os.getenv('SECRETE_KEY')
WTF_CSRF_SECRET_KEY = secrets.token_bytes()
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')