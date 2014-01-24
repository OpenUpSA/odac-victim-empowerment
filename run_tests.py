import msg_handler
import unittest


class MsgHandlerTestCase(unittest.TestCase):

    def setUp(self):
        msg_handler.app.config['TESTING'] = True
        self.app = msg_handler.app.test_client()

    def send_msg(self):
        f = open('msg_handler/msg_example.json', 'r')
        msg = f.read()
        return self.app.post('/message/', data=msg).data

    def test_message_handler(self):
        """
        Check the contents of the response, after hitting the server with a message.
        """
        assert 'OK' in self.send_msg()

    # TODO: handle Redis connection while testing
    # def test_populated_cache(self):
    #     """
    #     Check that a user's details are retained in the cache, after sending a message.
    #     """
    #     tmp = self.send_msg()
    #     rv = self.app.get('/')
    #     assert '+27738257667' in rv.data


if __name__ == '__main__':
    unittest.main()