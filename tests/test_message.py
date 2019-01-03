import coeus_test.message as message
import unittest


class MessageTestCase(unittest.TestCase):

    @staticmethod
    def message_init_no_message_type():
        message.Message(None, None)

    @staticmethod
    def message_init_no_payload():
        message.Message('message_type', None)

    @staticmethod
    def message_init_non_dict_payload():
        message.Message('message_type', [])

    def test_message_init_raises_exception_when_missing_message_type(self):
        self.assertRaises(ValueError, MessageTestCase.message_init_no_message_type)

    def test_message_init_raises_exception_when_missing_payload(self):
        self.assertRaises(ValueError, MessageTestCase.message_init_no_payload)

    def test_message_init_raises_exception_when_non_dict_payload(self):
        self.assertRaises(ValueError, MessageTestCase.message_init_non_dict_payload)