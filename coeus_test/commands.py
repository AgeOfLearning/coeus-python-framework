import message

DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_ENTITY_REGISTERED = True


def assert_verify_message(message):
    """
    Verifies that the message is not None,
    'payload' exists and 'payload' is not None.
    :param message:
    :return:
    """
    assert message is not None
    assert 'payload' in message
    assert message['payload'] is not None


def query_entity_is_registered(cli, entity_id):
    """
    Requests status on whether an entity is registered or not.
    :param cli:
    :param entity_id:
    :return: bool
    """

    message_payload = {
        "entity_id": entity_id
    }
    msg = message.Message("query.entity.isRegistered", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    assert_verify_message(response)
    return bool(response['payload']['result'])


def await_entity_registered(cli, entity_id, is_registered=DEFAULT_ENTITY_REGISTERED, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Waits for an entity to become registered, then continues.
    :param cli:
    :param entity_id:
    :param is_registered: Whether or not to await for registered state (True | False)
    :param timeout_seconds: How long until this returns with failure
    :return: bool
    """
    message_payload = {
        "entity_id": entity_id,
        "is_registered": is_registered,
        "timeout": timeout_seconds
    }
    msg = message.Message("await.entity.registered", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    assert_verify_message(response)
    return bool(response['payload']['success'])


def fetch_entity(cli, entity_id):
    """
    Fetches a serialized representation of the entity. If it is
    ITestEntity<T>, then the model is serialized as well.
    :param cli:
    :param entity_id:
    :return: {} payload
    """
    message_payload = {
        "entity_id": entity_id
    }
    msg = message.Message("fetch.entity", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    assert_verify_message(response)
    return response['payload']


def invoke_entity_method(cli, entity_id, method_name, parameters):
    """
    Invokes a method on the ITestEntity. It then returns the serialized
    value.
    :param cli:
    :param entity_id:
    :param method_name:
    :param parameters:
    :return:
    """
    message_payload = {
        "entity_id": entity_id,
        "method_name": method_name,
        "parameters": parameters
    }
    msg = message.Message("invoke.entity.method", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    assert_verify_message(response)
    assert response['payload']['is_error'] is False, response['payload']['error_message']
    return response['payload']['result']
