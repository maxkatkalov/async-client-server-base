import pytest
import aiohttp
from aioresponses import aioresponses
from client import get_models

BASE_URL = "http://127.0.0.1:8080/"


@pytest.mark.asyncio
async def test_get_models_success():
    # Створюємо об'єкт aioresponses для обробки HTTP-відповідей
    with aioresponses() as mocked_responses:
        # Встановлюємо штучну відповідь для запиту до BASE_URL
        mocked_responses.get(BASE_URL, payload={"your": "json", "data": "here"}, status=200)

        # Викликаємо тестову функцію
        status = await get_models()
        assert status == 200


@pytest.mark.asyncio
async def test_get_models_empty_response():
    # Створюємо об'єкт aioresponses для обробки HTTP-відповідей
    with aioresponses() as mocked_responses:
        # Встановлюємо штучну відповідь для запиту до BASE_URL з пустим вмістом
        mocked_responses.get(BASE_URL, payload={}, status=200)

        # Викликаємо тестову функцію
        status = await get_models()

        # Перевіряємо, що статус відповіді є 200
        assert status == 200


@pytest.mark.asyncio
async def test_get_models_error():
    # Створюємо об'єкт aioresponses для обробки HTTP-відповідей
    with aioresponses() as mocked_responses:
        # Встановлюємо штучну відповідь для запиту до BASE_URL з помилковим статусом
        mocked_responses.get(BASE_URL, status=404)

        # Викликаємо тестову функцію
        status = await get_models()

        # Перевіряємо, що статус відповіді є 404
        assert status == 404

if __name__ == '__main__':
    pytest.main()
