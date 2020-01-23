# -*- coding: utf-8 -*-
"""Application configuration."""
from os import environ


class Config(object):
    """Base configuration."""
    # SWAGGER
    SWAGGER_URL = environ.get('SWAGGER_URL', '/cashier/docs')
    SWAGGER_FILE_PATH = environ.get('SWAGGER_FILE_PATH', '/swagger.yml')
    # APPLICATION
    APP_NAME = environ.get('APP_NAME', 'Cashier Service API')
    PORT = environ.get('PORT', 5004)
    TOPIC_NAME = environ.get('TRANSACTIONS_TOPIC_ID')
    PROJECT_ID = environ.get('PROJECT_ID')


class DevConfig(Config):
    """Development configuration."""

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION. ')


class Testing(Config):
    """Testing configuration."""

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


config = {
    'development': DevConfig,
    'testing': Testing
}
