import json
from http import HTTPStatus

from behave import when, then


@when('I make a "{tx_type}" request for amount {amount:d} to account "{account}"')  # noqa
def make_request(context, tx_type, amount, account):
    payload = dict(accountNumber=account, amount=amount, operation=tx_type)
    context.response = context.web_client.post('/cashier/create', json=payload)


@then(u'I should receive an "Accepted" response')
def assert_response(context):
    response = context.response
    status_code = response.status_code
    assert status_code == HTTPStatus.ACCEPTED.value, \
        f'Expected status code to be 201; got {status_code}'

    response = context.response.get_json()
    assert response['status'] == 'accepted', repr(response)


@then('a "{tx_type}" request should have been published for account "{account}" with amount {amount:d}')  # noqa
def assert_transaction_event_published(context, tx_type, account, amount):
    events = context.broker

    event = json.loads(events.last_event)
    assert event['accountNumber'] == account, f"{event['accountNumber']} != {account}"  # noqa
    assert event['operation'] == tx_type, f"{event['operation']} != {tx_type}"
    assert event['status'] == 'accepted'
    assert event['amount'] == amount, f"{event['amount']} != {amount}"
