import random

import allure
import datetime

import pytest
from dotenv import load_dotenv

load_dotenv()


@allure.epic("NASA API Tests")
@allure.feature("APOD")
class TestAPOD:

    @allure.story("Basic API test")
    @pytest.mark.parametrize("field", ["title", "date", "explanation", "url"])
    def test_apod_basic(self, field, make_request):
        data = make_request()
        assert field in data, f'{field} field is missing in response'


class TestsAPODDateField:

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

    @allure.story("Invalid date format test")
    def test_wrong_date(self, make_request):
        incorrect_date = '2024-13-01'
        make_request(params={"date": incorrect_date}, expected_status=400)

    @allure.story("Request images for a short date range")
    def test_range_dates(self, make_request):
        start_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=random.randrange(10, 30))
        end_date = (start_date + datetime.timedelta(days=random.randrange(7))).strftime('%Y-%m-%d')
        data = make_request(params={"start_date": start_date.strftime('%Y-%m-%d'), "end_date": end_date})
        assert isinstance(data, list), "Expected a list of images, but received a different type"
        assert len(data) > 1, "Expected at least 2 images, but received fewer"
        assert data[0]["date"] != data[-1]["date"], "Expected unique dates in images, but received duplicates"
