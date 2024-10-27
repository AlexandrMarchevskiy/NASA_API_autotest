import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
url = "https://api.nasa.gov/planetary/apod"

@pytest.mark.parametrize("field", ["title", "date", "explanation", "url"])
def test_apod_basic(field):
    params = {"api_key": NASA_API_KEY}
    response = requests.get(url, params=params)
    status_code = response.status_code

    assert status_code == 200, f'Status code is not 200, got {status_code}'

    data = response.json()
    assert field in data, f'{field} field is missing in response'


