from time import time

import ParserUtil
import RequestsUtil

CACHE_TIME = 120


class RouterAPI:
    def __init__(self, username, password):
        RequestsUtil.login(username, password)

        self.connections = None
        self.connections_time = 0

        self.status = None
        self.status_time = 0

    def get_connections(self, force=None):
        if force or not self.connections or (self.connections_time + CACHE_TIME) < time():
            self.connections = ParserUtil.parse_connections(RequestsUtil.get_connections_html())
            self.connections_time = time()

        return self.connections

    def get_status(self, force=None):
        if force or not self.status or (self.status_time + CACHE_TIME) < time():
            self.status = ParserUtil.parse_status(RequestsUtil.get_status_html())
            self.status_time = time()

        return self.status

