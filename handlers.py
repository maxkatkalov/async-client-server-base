import json

import aiohttp
from aiohttp import web
import aiofiles

from server import app, routes


async def read_write_to_file(
        filename: str = "brands.json",
        mode: str = "w",
        action: str = "write",
        data: str = None
) -> None:
    if action == "read":
        async with aiofiles.open(filename, "r") as file:
            return await file.read()
    async with aiofiles.open(filename, mode) as file:
        await file.write(data)


@routes.get('/', name="models")
async def return_models(request: aiohttp.request) -> aiohttp.web.Response:
    data = await read_write_to_file(action="read", mode="r")
    if data:
        return web.Response(body=data, content_type="application/json")
    null_response = json.dumps({"response": "No brands now."})
    return web.Response(body=null_response, content_type="application/json", status=200)


@routes.post("/", name="add_new_model")
async def add_new_model(request: aiohttp.request) -> aiohttp.web.Response:
    content = await request.post()
    content_dict = dict(content)
    if (
            (brand := content_dict.get("brand")) and
            (country := content_dict.get("country"))
    ):
        existing_data = await read_write_to_file(action="read")
        existing_data_list = json.loads(existing_data)
        new_data = {"brand": brand, "country": country}
        existing_data_list.append(new_data)
        updated_data = json.dumps(existing_data_list, indent=4)

        await read_write_to_file(data=updated_data)

        return web.Response(text="New model created!", status=201)

    return web.Response(
        text="Data incorrect. Please pass model name and country!",
        status=400,
    )

app.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app)
