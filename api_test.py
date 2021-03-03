import time

import requests
import asyncio
from aiohttp import ClientSession

url = "http://119.3.200.75:8065/dictionary/F299F8B7-76D1-37BE-384C-C414DE6FC704"

url2 = "http://119.3.200.75:8055/openapi/kb/chinese-patent-medicine/list?key=%E5%BD%93%E5%BD%92"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
}

tasks = []


# 协程调用
async def get_response():
    async with ClientSession() as session:
        async with session.get(url2, headers=headers) as response:
            response = await response.read()
            print(response)
            print(time.time())


def run():
    for i in range(50):
        task = asyncio.ensure_future(get_response())
        tasks.append(task)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run()
    loop.run_until_complete(asyncio.wait(tasks))
