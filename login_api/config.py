# logindemoapi/config.py

import os

class Config:
    # DB URL is being taken from environment variable.
    # Some reason, if I change the db file location to another folder it is not working.
    # For example, if I put the db file in the 'login_api/db/' folder, it is not working.
    # It is working only if I put the db file in the instance folder.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///db/LoginDemo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # You might add secret keys, other environment variables here
    SECRET_KEY = os.environ.get('SECRET_KEY') # or 'a_very_secret_key_that_should_be_in_env'