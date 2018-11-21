import unittest
import coeus.client


class ClientTestCase(unittest.TestCase):
    @staticmethod
    def client_init_none_tcp_ip():
        coeus.client.Client(tcp_ip=None)

    @staticmethod
    def client_init_none_tcp_port():
        coeus.client.Client(tcp_port=None)

    @staticmethod
    def client_send_message_none_message():
        cli = coeus.client.Client()
        cli.send_message(None)

    def test_client_init_raises_exception_when_none_tcp_ip(self):
        self.assertRaises(ValueError, ClientTestCase.client_init_none_tcp_ip)

    def test_client_init_raises_exception_when_none_tcp_port(self):
        self.assertRaises(ValueError, ClientTestCase.client_init_none_tcp_port)

    def test_client_send_message_raises_exception_when_none_message(self):
        self.assertRaises(ValueError, ClientTestCase.client_send_message_none_message)