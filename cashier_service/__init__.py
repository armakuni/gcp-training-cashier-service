"""Main application package."""

from os import path

from flask_swagger_ui import get_swaggerui_blueprint
from yaml import Loader, load

from cashier_service.settings import Config


def setup_swagger():

    swagger_yml = load(
        open(get_app_base_path() + Config.SWAGGER_FILE_PATH, 'r'),
        Loader=Loader)

    swaggerui_blueprint = get_swaggerui_blueprint(
        Config.SWAGGER_URL,
        '',
        config={
            'app_name': Config.APP_NAME,
            'spec': swagger_yml
        },
    )

    return swaggerui_blueprint


def get_app_base_path():
    return path.dirname(path.dirname(path.realpath(__file__)))
