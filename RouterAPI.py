from time import time

from utils import ParserUtil
from utils import RequestsUtil

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

    def ping(self, target):
        return ParserUtil.parse_diagnostic_responce(RequestsUtil.diagnostic_ping_html(target, 1))

    def ping_ipv6(self, target):
        return ParserUtil.parse_diagnostic_responce(RequestsUtil.diagnostic_ping_html(target, 2))

    def traceroute(self, target):
        return ParserUtil.parse_diagnostic_responce(RequestsUtil.diagnostic_ping_html(target, 4))

    def traceroute_ipv6(self, target):
        return ParserUtil.parse_diagnostic_responce(RequestsUtil.diagnostic_ping_html(target, 3))

    def diag_get_atm_status(self):
        return ParserUtil.parse_diagnostic_responce(RequestsUtil.diagnostic_dsl_html(1))

    def diag_get_atm_loopback_test(self):
        return ParserUtil.parse_diagnostic_responce(RequestsUtil.diagnostic_dsl_html(2))

    def diag_get_dls_line_status(self):
        return ParserUtil.parse_diagnostic_responce(RequestsUtil.diagnostic_dsl_html(3))

    def diag_reset_adsl_line(self):
        return ParserUtil.parse_diagnostic_responce(RequestsUtil.diagnostic_dsl_html(4))