import allure
import os

import pytest
import requests


@pytest.fixture
def make_request():
    api_key = os.getenv("NASA_API_KEY")
    url = "https://api.nasa.gov/planetary/apod"

    @allure.step("Making request to NASA APOD API")
    def _make_request(params=None, expected_status=200):
        base_params = {"api_key": api_key}
        if params:
            base_params.update(params)

        response = requests.get(url, params=base_params)

        status_code = response.status_code
        assert status_code == expected_status, f'Status code is not 200, got {expected_status}'

        return response.json()

    return _make_request
