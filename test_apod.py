import allure
import datetime
import os

import pytest
from dotenv import load_dotenv

load_dotenv()

@allure.epic("NASA API Tests")
@allure.feature("APOD")
class TestAPOD:
    NASA_API_KEY = os.getenv("NASA_API_KEY")
    url = "https://api.nasa.gov/planetary/apod"

    @allure.story("Basic API test")
    @pytest.mark.parametrize("field", ["title", "date", "explanation", "url"])
    def test_apod_basic(self, field, make_request):
        data = make_request()
        assert field in data, f'{field} field is missing in response'

    @allure.story("Date field test")
    def test_apod_date_field(self, make_request):
        data = make_request()
        expected_date = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d')
        assert data["date"] == expected_date

    @allure.story("Past date test")
    def test_apod_past_date(self, make_request):
        past_date = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        data = make_request(params={"date": past_date})
        assert data["date"] == past_date, f'Expected date {past_date}, but got {data["date"]}'
