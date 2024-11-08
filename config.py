import os


class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    REPO_TYPE = os.getenv('REPO_TYPE', 'in_memory')


class DevelopmentConfig(Config):
    """Development configuration with SQLite database and debugging enabled."""
    REPO_TYPE = os.getenv('REPO_TYPE', 'in_SQLite_db')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing configuration with testing flag enabled."""
    TESTING = True


class ProductionConfig(Config):
    """Production configuration with MySQL database and debugging disabled."""
    REPO_TYPE = os.getenv('REPO_TYPE', 'in_MySQL_db')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://admin:admin@localhost:5432/production_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
