import asyncio

import pytest
from aiohttp import web


from handlers import return_models, add_new_model, read_write_to_file


@pytest.fixture
@pytest.mark.asyncio
async def setup_teardown_file():
    # Збереження початкового стану файлу
    original_data = await read_write_to_file(action="read")
    print(original_data)
    yield
    await read_write_to_file(data=original_data)


@pytest.fixture
@pytest.mark.asyncio
async def create_app(aiohttp_client):
    app = web.Application()
    app.router.add_get("/", return_models)
    app.router.add_post("/", add_new_model)
    client = await aiohttp_client(app)
    return client


@pytest.mark.asyncio
async def test_response_status(create_app):
    client = await create_app
    response = await client.get("/")
    assert response.status == 200


@pytest.mark.parametrize(
    "test_data, expected_code, expected_message",
    (
        pytest.param(
            {"country": "Ukraine"},
            400,
            "Data incorrect. Please pass model name and country!",
            id="Response without 'brand'"
        ),
        pytest.param(
            {"brand": "New one"},
            400,
            "Data incorrect. Please pass model name and country!",
            id="Response without 'country'"
        ),
        pytest.param(
            {},
            400,
            "Data incorrect. Please pass model name and country!",
            id="Response with any info"
        ),
        pytest.param(
            {"brand": "", "country": ""},
            400,
            "Data incorrect. Please pass model name and country!",
            id="Response with any info"
        ),
        pytest.param(
            {"brand": "New one", "country": "Ukraine"},
            201,
            "New model created!",
            id="Response with full data"
        ),
    )
)
@pytest.mark.asyncio
async def test_add_new_model(
        setup_teardown_file,
        create_app,
        test_data,
        expected_code,
        expected_message
):
    client = await create_app
    response = await client.post("/", data=test_data)
    assert expected_code == response.status
    assert expected_message in await response.text()

if __name__ == '__main__':
    pytest.main()
