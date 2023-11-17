import asyncio

import aiohttp
from aiohttp.web_response import Response


BASE_URL = "http://127.0.0.1:8080/"


async def get_models() -> Response.status:
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL) as response:
            content = await response.json()
            if content:
                print(content)
                return response
            print("Page not found!")
            return response.status


if __name__ == '__main__':
    asyncio.run(get_models())
