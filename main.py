import asyncio

from aiohttp import web

from handlers import app
from client import get_models


if __name__ == '__main__':
    web.run_app(app)
    asyncio.run(get_models())
