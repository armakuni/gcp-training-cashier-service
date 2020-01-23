from flask import Blueprint, jsonify
import logging

health = Blueprint('health', __name__, url_prefix='/cashier/')


@health.route('/health')
def get_health():
    logging.info("Health check request")
    return jsonify(message='OK')
