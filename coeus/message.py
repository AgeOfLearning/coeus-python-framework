#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Message:
    """
    Represents a message that is serialized to json as {'type':..., 'payload':...}
    """

    type = None
    payload = None

    def __init__(self, message_type, payload):
        self.type = message_type
        self.payload = payload
