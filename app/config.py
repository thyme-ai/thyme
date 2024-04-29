from os import environ

class Configuration:
    URI = environ.get('DATABASE_URL')

    # TODO - Un-comment once using Heroku PostgreSQL database
    # Adjustments to Databsae URI required for Heroku to Work with SQLAlchemy
    # if URI.startswith("postgres://"):
    #     URI = URI.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY')
    GOOGLE_CLIENT_CONFIG= environ.get('GOOGLE_CLIENT_CONFIG')
    OAUTHLIB_INSECURE_TRANSPORT = environ.get('OAUTHLIB_INSECURE_TRANSPORT')