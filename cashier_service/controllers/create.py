from datetime import datetime
from http import HTTPStatus
from json import dumps
from uuid import uuid4

from flask import current_app, Blueprint, jsonify, request, send_from_directory
from schema import Schema, And, SchemaError

from cashier_service import get_app_base_path

process = Blueprint('process', __name__, url_prefix='/cashier/')

PAYLOAD_SCHEMA = Schema(dict(accountNumber=And(str, lambda s: len(s) == 8),
                             amount=And(int, lambda n: n > 0),
                             operation=lambda s: s in ['credit', 'debit']))

@process.route('/create', methods=['POST'])
def process_cashier_requests():
    if not request.is_json:
        raise ContentTypeError()

    req_data = request.get_json()

    PAYLOAD_SCHEMA.validate(req_data)

    operation_id = str(uuid4())
    created = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    account_number = req_data['accountNumber']
    amount = req_data['amount']
    operation = req_data['operation']

    broker = current_app.broker
    try:
        broker.produce(dumps(dict(id=operation_id,
                                  accountNumber=account_number,
                                  amount=amount,
                                  operation=operation,
                                  status='accepted',
                                  created=created)))
    except Exception:
        raise FailedToPublishError()

    return jsonify(
        id=operation_id,
        accountNumber=account_number,
        amount=amount,
        status='accepted',
        operation=operation,
        created=created), HTTPStatus.ACCEPTED

@process.route('/swagger.yml', methods=['GET'])
def get_swagger():
    return send_from_directory(get_app_base_path(), 'swagger.yml')


class ContentTypeError(RuntimeError):
    pass

class FailedToPublishError(RuntimeError):
    pass

@process.errorhandler(SchemaError)
def schema_error(e):
    return jsonify(message=str(e)), HTTPStatus.BAD_REQUEST

@process.errorhandler(ContentTypeError)
def content_type_error(e):
    return jsonify(message='Request must be JSON'), \
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE

@process.errorhandler(FailedToPublishError)
def failed_to_publish_error(e):
    return jsonify(message="Failed to process transaction"), HTTPStatus.INTERNAL_SERVER_ERROR
