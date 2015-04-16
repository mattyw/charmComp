#!/usr/bin/env python

import os
import socket
import SocketServer as ss
import threading
import time


def _read_all(sock):
    data = b''
    try:
        while True:
            d = sock.recv(1024)
            if not d:
                break
            data += data
    except socket.timeout:
        pass
    return data


def send(host, port, msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    sock.connect((host, port))
    try:
        sock.sendall(msg)
        result = _read_all(sock)
    finally:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    if result.startswith('ERROR: '):
        raise Exception(result[7:])
    return result


class DataStore(object):

    def __init__(self, host, port, series, verbose=False):
        self.host = host
        self.port = port
        self.series = series
        self.verbose = verbose

    def store_data(self, number, timestamp=None, series=None):
        if timestamp is None:
            timestamp = time.time()
        if series is None:
            series = self.series
        msg = '{} {} {}'.format(series, number, int(timestamp))

        if self.verbose:
            print('sending message:\n' + msg)
        send(self.host, self.port, msg)


class _Handler(ss.BaseRequestHandler):

    store = None

    def _parse(self):
        data = b''
        while True:
            d = self.request.recv(1024)
            if not d:
                break
            data += d
        series, _, number = data.encode('utf-8').rpartition(':')

        try:
            value = int(number)
        except ValueError:
            raise Exception('expected a number, got {!r}'.format(number))

        if value < 0 or value > 100:
            raise Exception('out of bounds [0, 100]: {}'.format(value))

        if not series:
            series = None
        return number, series

    def handle(self):
        try:
            number, series = self._parse()
            self.store.store_data(number, series=series)
        except Exception as e:
            raise
            msg = 'ERROR: {}'.format(e).decode('utf-8')
        else:
            msg = ''  # success

        self.request.sendall(msg)


class Server(ss.TCPServer):

    daemon_threads = True  # support C-C
    allow_reuse_address = True

    @classmethod
    def from_addrs(cls, targethost, targetport, host, port, series,
                   verbose=False):
        #verbose = True
        store = DataStore(targethost, targetport, series, verbose)
        server = cls(host, port, store)
        return server

    def __init__(self, host, port, store):
        _store = store
        class handler(_Handler):
            store = _store
        ss.TCPServer.__init__(self, (host, port), handler)

        self.thread = threading.Thread(target=self.serve_forever)
        self.thread.daemon = True

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.shutdown()

    def start(self):
        self.thread.start()

    def run(self, timeout=None):
        self.start()
        with self:
            self.thread.join(timeout)

    def daemon(self):
        raise NotImplementedError

    def pid(self):
        return os.getpid()


class ForkingServer(ss.ForkingMixIn, Server):
    pass


class ThreadingServer(ss.ThreadingMixIn, Server):
    pass


def main(targethost, targetport, host, port, ns):
    _Server = ThreadingServer
    #Server = ForkingServer
    server = _Server.from_addrs(targethost, targetport, host, port, ns)

    print(server.pid())
    server.run()


if __name__ == '__main__':
    import argparse

    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = 9999
    DEFAULT_NAMESPACE = ''

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=DEFAULT_HOST,
                        help='the address of the data store server')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT,
                        help='the port of the data store server')
    parser.add_argument('--ns', default=DEFAULT_NAMESPACE,
                        help='the DB namespace to target')
    parser.add_argument('targethost',
                        help='the address of the data store server')
    parser.add_argument('targetport', type=int,
                        help='the port of the data store server')
    args = parser.parse_args()

    srv = main(args.host, args.port, args.targethost, args.targetport, args.ns)
