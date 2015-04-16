import random
#import socket
import SocketServer as ss
import unittest

import server


HOST = '127.0.0.1'
TPORT = 9998
PORT = 9999
SERIES = 'test'


class FakeHandler(ss.BaseRequestHandler):

    def handle(self):
        self.msg = self.request.recv(1024).encode('utf-8')


class BaseSuite(unittest.TestCase):

    def setUp(self):
        super(BaseSuite, self).setUp()

        self.handlers = []
        self.sent = []

        self.numbers = [random.randint(1, 20) for _ in range(9)]

    @property
    def handler(self):
        try:
            return self.handlers[-1]
        except IndexError:
            return None

    def _new_handler(self, *args, **kwargs):
        handler = FakeHandler(*args, **kwargs)
        self.handlers.append(handler)
        return handler

    def new_server(self, port):
        return ss.TCPServer((HOST, port), self._new_handler)

    def send(self, host, port, data):
        self.sent.append((host, port, data))


class TestDataStore(BaseSuite):

    def test_stuff(self):
        pass


class TestServer(BaseSuite):

    def test_run(self):
        pass

    def test_run_background(self):
        pass

    def test_(self):
        pass


class TestMain(BaseSuite):

    def test_okay(self):
        send = server.send
        server.send = self.send
        try:
            srv = server.main(HOST, TPORT, HOST, PORT, SERIES)
            send(HOST, PORT, b'10')
            srv.shutdown()
        finally:
            server.send = send

        self.assertEqual(len(self.sent), 1)
        sent, = self.sent
        host, port, msg = sent
        self.assertEqual(host, HOST)
        self.assertEqual(port, TPORT)

        series, number, timestamp = msg.encode('utf-8').split()
        self.assertEqual(series, 'test')
        self.assertEqual(number, '10')
        self.assertEqual(timestamp, '')


if __name__ == '__main__':
    unittest.main()
