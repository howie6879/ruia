import asyncio

from ruia import Request


async def request_example():
    url = "https://httpbin.org/get"
    params = {"name": "ruia"}
    headers = {"User-Agent": "Python3.6"}
    request = Request(
        url=url, method="GET", res_type="json", params=params, headers=headers
    )
    response = await request.fetch()
    assert await response.text()["args"]["name"] == "ruia"
    assert await response.text()["headers"]["User-Agent"] == "Python3.6"


def test_request():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(request_example())
    loop.close()
