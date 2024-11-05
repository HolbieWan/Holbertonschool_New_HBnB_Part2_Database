import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    REPO_TYPE = os.getenv('REPO_TYPE', 'in_file')

class DevelopmentConfig(Config):
    REPO_TYPE = os.getenv('REPO_TYPE', 'in_SQLite_db')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    REPO_TYPE = os.getenv('REPO_TYPE', 'in_MySQL_db')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin@localhost:5432/production_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}