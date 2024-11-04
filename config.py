import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    REPO_TYPE = os.getenv('REPO_TYPE', 'in_memory')

class DevelopmentConfig(Config):
    REPO_TYPE = os.getenv('REPO_TYPE', 'in_file')

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    REPO_TYPE = os.getenv('REPO_TYPE', 'in_sqlite_db')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}