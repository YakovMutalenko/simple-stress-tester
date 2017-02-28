#!/usr/bin/env python3
import argparse
from collections import Counter

from twisted.internet import epollreactor

# Should do this before any connections,
# listeners or connectors are added
epollreactor.install()

import treq
from twisted.internet import reactor, task
from twisted.web.client import HTTPConnectionPool

pool = HTTPConnectionPool(reactor)
cooperator = task.Cooperator()


class Tester:
    def __init__(self, url):
        self._stat = Counter(generated=0, sent=0, received=0)
        self.url = url

    @property
    def stat(self):
        return self._stat

    def body_received(self, body):
        self._stat['received'] += 1

    def request_sent(self, response):
        self._stat['sent'] += 1

        d = treq.text_content(response)
        d.addCallback(self.body_received)
        d.addErrback(lambda x: None)  # ignore errors

        return d

    def request(self):
        """Make a GET request"""

        d = treq.get(self.url, pool=pool)
        d.addCallback(self.request_sent)
        d.addErrback(lambda x: None)  # ignore errors

        return d

    def generate_requests(self):
        """Generate tens of thousands of requests"""

        while True:
            self.request()
            self._stat['generated'] += 1

            # do not yield deferred here so cooperator won't pause until
            # response is received
            yield None

    def start(self):
        """Make cooperator work on spawning requests"""

        iterator = self.generate_requests()
        cooperator.cooperate(iterator)


def show_progress(stat):
    """Print the progress at one second intervals"""

    print(', '.join('{} {}'.format(k, v) for k, v in stat.items()))

    reactor.callLater(1, show_progress, stat)


if __name__ == '__main__':
    # parse args from command-line interface
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, help='A custom URL to bombard')
    args = parser.parse_args()

    # start a long-running cooperative task
    tester = Tester(args.url)
    tester.start()

    # run the counter that will be reporting sending speed once a second
    reactor.callLater(1, show_progress, tester.stat)

    # run the reactor
    reactor.run()
