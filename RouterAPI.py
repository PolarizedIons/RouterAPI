from time import time

import ParserUtil
import RequestsUtil

CACHE_TIME = 120


class RouterAPI:
    def __init__(self, username, password):
        RequestsUtil.login(username, password)

        self.status = None
        self.status_time = 0

    def get_status(self, force=None):
        if force or not self.status or (self.status_time + CACHE_TIME) < time():
            self.status = ParserUtil.parse_status(RequestsUtil.get_status_html())
            self.status_time = time()

        return self.status

