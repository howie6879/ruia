#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/10.
 pip install ruia_shell
"""
from ruia_shell import inspect_ruia

from ruia import Spider


class InspectSpider(Spider):
    start_urls = ["http://httpbin.org/get"]

    async def parse(self, response):
        # Debug here
        inspect_ruia(self, response.url)


if __name__ == "__main__":
    InspectSpider.start()
