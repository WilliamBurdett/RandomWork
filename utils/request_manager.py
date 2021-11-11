import time
from datetime import datetime, timedelta

import requests


class RequestManager:
    def __init__(self, logger):
        self.last_request = datetime.now()
        # Up to 4 requests per second, this gives between 3 and 4.
        self.request_throttle = 300
        self.logger = logger

    def ready_to_make_request(self):
        while (
            self.last_request + timedelta(microseconds=self.request_throttle)
            > datetime.now()
        ):
            time.sleep(self.request_throttle)

    def make_request(self, url: str):
        self.ready_to_make_request()
        self.last_request = datetime.now()
        response = requests.get(url)
        if "error" in response.json().keys():
            self.logger.critical(response.json())
        return response

    def stream(self, url: str):
        self.ready_to_make_request()
        return requests.get(url, stream=True)
