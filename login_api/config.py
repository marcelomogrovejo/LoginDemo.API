# logindemoapi/config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///LoginDemo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # You might add secret keys, other environment variables here
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_that_should_be_in_env'