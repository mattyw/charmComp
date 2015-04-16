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

    def check_sent(self, series, numbers):
        self.assertEqual(len(self.sent), len(numbers))

        for sent, num in zip(self.sent, numbers):
            host, port, msg = sent
            self.assertEqual(host, HOST)
            self.assertEqual(port, TPORT)

            series, number, timestamp = msg.encode('utf-8').split()
            self.assertEqual(series, 'test')
            self.assertEqual(number, str(num))
            self.assertEqual(timestamp, '')

    def test_send(self):
        numbers = [10, 100, 99, 7, 42]

        send = server.send
        server.send = self.send
        try:
            srv = server.Server.from_addrs(HOST, TPORT, HOST, PORT, SERIES)
            srv.start()
            with srv:
                for num in numbers:
                    send(HOST, PORT, bytes(str('10')))
        finally:
            server.send = send

        self.check_sent(SERIES, numbers)

    def test_run(self):
        pass


if __name__ == '__main__':
    unittest.main()
