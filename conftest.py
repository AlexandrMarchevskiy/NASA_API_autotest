import os

import pytest
import requests


@pytest.fixture
def make_request():
    api_key = os.getenv("NASA_API_KEY")
    url = "https://api.nasa.gov/planetary/apod"

    def _make_request(params=None):
        base_params = {"api_key": api_key}
        if params:
            base_params.update(params)

        response = requests.get(url, params=base_params)

        status_code = response.status_code
        assert status_code == 200, f'Status code is not 200, got {status_code}'

        return response.json()

    return _make_request