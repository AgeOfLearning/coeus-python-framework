# coeus
*coeus* is a python client implementation of the json-message protocol for remote (Tcp) integration tests.

[pypi-build-status]: https://img.shields.io/pypi/v/coeus-test.svg
[travis-ci-status]: https://img.shields.io/travis/AgeOfLearning/coeus-python-framework.svg

[![pypi][pypi-build-status]](https://pypi.python.org/pypi/coeus-test)
[![travis][travis-ci-status]](https://travis-ci.org/AgeOfLearning/coeus-python-framework)

## Installation
*coeus* is meant to be added as a requirement to your python unit-test project. Simply add a reference to `coeus-test`.

`pip install coeus-test`

## Getting Started

### Glossary
**Client**: A class for connecting via TCP to the server application.

**Message**: A specific json format (prototcol) defining the communication.

**TestEntity**: An abstract concept for an `entity` that exists in the server application. Usually accessed via it's ID.

### Client Setup
The client must connect to the server application via an IP and port. You can invoke a connection as follows:

```python
import client

cli = client.Client(tcp_port=31203)
cli.connect()
```

By default, it will attempt to connect with ip: `127.0.0.1`. 

## Commands
Commands are specific blocking calls that are sent to the server, then waits to receive a message. Every command has a response. 

>Commands do not handle any validation of message received from unity client.

```python
import commands
```
### Query Commands

#### query_entity_is_registered
This command asks the unity application about the state of an entity. 

>Usage
```python
result = commands.query_entity_is_registered(cli, "myEntityId")
```

>Response
```json
{
    "type" : "query.entity.isRegistered",
    "payload": {
        "result" : true | false
    }
}
```

### Await Commands

#### await_entity_registered
This command blocks until a specific state is reached for the entitiy. By default, it will block until the entity was registered. If the command exceeds the specified timeout, it continue with a failure.

>Usage
```python
// is_registered, timeout_seconds optional...
result = commands.await_entity_registered(cli, "myEntityId", is_registered=True, timeout_seconds=60)
```

>Response
```json
{
    "type":"await.continue",
    "payload": {
        "success":true|false
    }
}
```

### Fetch Commands

#### fetch_entity
This command asks the server to serialize the TestEntity and send it. 

>Usage
```python
result = commands.fetch_entity(cli, "myEntityId")
```

>Success Response
```json
{
    "type":"fetch.entity",
    "payload": {
        "test_entity" : {...} | null
    }
}
```

### Invoke Commands

#### invoke_entity_method
This command allows the python unit-test to invoke a method on the server"s TestEntity and return the result.

>Usage
```python
parameters = {
    "statName":"score"
}
result = commands.invoke_entity_method(cli, "myEntityId", "GetPlayerStat", parameters)
```

In the C# code, this will look for a method with the following signature:
```csharp
public int GetPlayerStat(IDynamicObject parameters)
{
    var statName = parameters.GetValue<string>("statName");
    ...

    return stat;
}
```

>Response
```json
{
    "type":"invoke.entity.method",
    "payload": {
        "is_error" : false,
        "error_message" : null,
        "result" : 32
    }
}
```
If there is a C# exception, then the `error_message` will contain the exceptions message.

## Assertions
The commands do not validate the response from the server. To easily do this, use the assertions.

```python
import assertions

...
# Fails assert if False returned from response...
assertions.assert_entity_is_registered(cli, "myEntityId")

# Fails if timeout exceeded...
assertions.assert_await_entity_registered(cli, "myEntityId")

# Fails if the test_entity is None...
result = assertions.assert_fetch_entity(cli, "myEntityId")

# Fails if is_error == True, AssertException with message provided...
result = assert_invoke_entity_method(cli, "myEntityId", "GetPlayerStat", ...)
```
