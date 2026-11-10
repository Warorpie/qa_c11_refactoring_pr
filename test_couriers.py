"""
Тесты для процедурных хелперов из helpers.py.
Необъодимо переписать их под использование класса CourierAPIClient.
"""
import pytest
import requests
from api_client import CourierAPIClient
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5001/api")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "test_token_123")


@pytest.fixture
def new_courier_data():
    return {
        "first_name": "Мария",
        "last_name": "Сидорова",
        "phone": "+79997654321"
    }


@pytest.fixture
def client():
    return CourierAPIClient(base_url=BASE_URL, auth_token=AUTH_TOKEN)


@pytest.mark.usefixtures("fake_server")
class TestCourierHelpers:
    """Тесты для работы с курьерами (теперь через CourierAPIClient)."""

    def test_get_courier_by_id(self, client):
        courier = client.get_courier_by_id(1)
        assert courier["id"] == 1
        assert courier["first_name"] == "Иван"

    def test_create_courier(self, client, new_courier_data):
        result = client.create_courier(new_courier_data)
        assert "id" in result
        assert result["first_name"] == "Мария"

    def test_get_nonexistent_courier_raises(self, client):
        with pytest.raises(requests.exceptions.HTTPError):
            client.get_courier_by_id(99999)

    def test_delete_courier(self, client):
        result = client.delete_courier(2)
        assert result == {"status": "deleted"}
