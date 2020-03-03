import os

from application.utils import init_logger

# root dir of app:
basedir = os.path.abspath(os.path.dirname(__file__))

#  COMMON
#  ----------------------------------------------------------------
class Config:
    # security:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)

    # JWT configs:
    JWT_SECRET = os.environ.get('JWT_SECRET') or \
        'abc123abc1234'
    JWT_ALGORITHMS = 'HS256'

    # logger:
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or \
        'INFO'
    LOGGER = init_logger(__name__, LOG_LEVEL)

    @staticmethod
    def init_app(app):
        """ integrate with app factory
        """
        pass

#  DEVELOPMENT
#  ----------------------------------------------------------------
class DevelopmentConfig(Config):
    DEBUG = True

#  Testing
#  ----------------------------------------------------------------
class TestingConfig(Config):
    TESTING = True

    # enable url path generation in test cases:
    SERVER_NAME = 'localhost.localdomain'

#  PRODUCTION
#  ----------------------------------------------------------------
class ProductionConfig(Config):
    pass


#  CONFIG SELECTION
#  ----------------------------------------------------------------
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}