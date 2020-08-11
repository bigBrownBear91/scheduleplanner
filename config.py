import os
import secrets

SESSION_TYPE = 'filesystem'
SECRETE_KEY = os.getenv('SECRETE_KEY')
WTF_CSRF_SECRET_KEY = secrets.token_bytes()
SQLALCHEM_DATABASE_URI = os.getenv('SQLALCHEM_DATABASE_URI')