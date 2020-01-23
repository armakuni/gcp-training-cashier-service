from flask import Flask
from flask_cors import CORS

from cashier_service import setup_swagger, get_app_base_path
from cashier_service.settings import Config
from cashier_service.controllers.health import health
from cashier_service.controllers.create import process

def create(config, broker):
    app = Flask(__name__,
                static_folder=get_app_base_path(),
                static_url_path='')
    app.config.from_object(config)
    CORS(app, resources={r"/cashier/swagger.yml": {"origins": "*"}})
    app.broker = broker
    app.register_blueprint(health)
    app.register_blueprint(process)

    app.register_blueprint(setup_swagger(), url_prefix=Config.SWAGGER_URL)
    return app
