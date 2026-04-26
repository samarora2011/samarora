import json
import os
import sys

import pytest

from utils.driver_factory import DriverFactory

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture(scope="function")
def setup(request):
    config_path = os.path.join(PROJECT_ROOT, "config.json")
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    driver = DriverFactory.get_driver(config)
    request.cls.driver = driver
    yield
    driver.quit()
