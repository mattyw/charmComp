#!/usr/bin/env python

import os
import socket
import SocketServer as ss
import time
 

def send(host, port, msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    try:
        sock.sendall(msg)
        time.sleep(1)  # XXX why?
    finally:
        sock.close()


class DataStore(object):

    def __init__(self, host, port, nsname, verbose=False):
        self.host = host
        self.port = port
        self.nsname = nsname
        self.verbose = verbose

    def store_data(self, number, timestamp=None, nsname=None):
        if timestamp is None:
            timestamp = time.time()
        if nsname is None:
            nsname = self.nsname
        msg = '{} {} {}'.format(nsname, number, int(timestamp))

        if self.verbose:
            print('sending message:\n' + msg)
        send(self.host, self.port, msg, nsname)


class _Handler(ss.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        super(_Handler, self).__init__(request, client_address, server)
        self.store = server.store

    def _parse(self):
        data = self.request.recv(1024)
        nsname, _, number = data.encode('utf-8').rpartition(':')

        try:
            float(number)
        except ValueError:
            raise Exception('expected a number, got {!r}'.format(number))

        return number, nsname

    def handle(self):
        try:
            number, nsname = self._parse()
            self.store.store_data(number, nsname=nsname or None)
        except Exception as e:
            msg = 'ERROR: {}'.format(e).decode('utf-8')
        else:
            msg = ''  # success

        self.request.sendall(msg)


class Server(ss.TCPServer):

    def __init__(self, host, port, store):
        super(Server, self).__init__((host, port), self._handler)

        self.store = store

    def _handler(self, request, client_address, server):
        return _Handler(request, client_address, server)

    def run(self):
        self.serve_forever()

    def run_background(self):
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        #server.shutdown()

    def pid(self):
        return os.getpid()


class ForkingServer(ss.ForkingMixIn, Server):
    pass


class ThreadingServer(ss.ThreadingMixIn, Server):
    pass


def main(targethost, targetport, host, port, ns):
    store = DataStore(targethost, targetport, ns)
    server = ThreadingServer(host, port, store)
    #server = ForkingServer(host, port, store)

    print(server.pid())
    #server.run()
    server.run_background()


if __name__ == '__main__':
    import argparse

    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = 9999
    DEFAULT_NAMESPACE = ''

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=DEFAULT_HOST,
                        help='the address of the data store server')
    parser.add_argument('--port', default=DEFAULT_PORT,
                        help='the port of the data store server')
    parser.add_argument('--ns', default=DEFAULT_NAMESPACE,
                        help='the DB namespace to target')
    parser.add_argument('targethost',
                        help='the address of the data store server')
    parser.add_argument('targetport',
                        help='the port of the data store server')
    args = parser.parse_args()

    main(args.host, args.port, args.targethost, args.targetport, args.ns)
