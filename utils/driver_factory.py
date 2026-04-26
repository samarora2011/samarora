from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from helpers.webdriver_listener import WebDriverListener
from extensions.webdriver_extended import WebDriverExtended
import os
import requests


def _cached_chromedriver_path(driver_version: str | None = None) -> str | None:
    home_dir = os.path.expanduser("~")
    base_dir = os.path.join(home_dir, ".wdm", "drivers", "chromedriver", "win64")
    if driver_version:
        version_dirs = [driver_version]
    else:
        if not os.path.isdir(base_dir):
            return None
        version_dirs = sorted(os.listdir(base_dir), reverse=True)

    for version in version_dirs:
        cache_dir = os.path.join(base_dir, version, "chromedriver-win32")
        for candidate in ["chromedriver.exe", "chromedriver"]:
            path = os.path.join(cache_dir, candidate)
            if os.path.exists(path):
                return path
    return None


def _normalize_chromedriver_path(driver_path: str) -> str:
    if "THIRD_PARTY_NOTICES" in driver_path:
        return driver_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver.exe")
    return driver_path


class DriverFactory:
    @staticmethod
    def get_driver(config) -> WebDriverExtended:
        if config["browser"] == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("start-maximized")
            if config["headless_mode"] is True:
                options.add_argument("--headless")

            driver_version = os.environ.get("CHROMEDRIVER_VERSION", "147.0.7727.117")
            manager = ChromeDriverManager(driver_version=driver_version)

            try:
                driver_path = manager.install()
            except requests.exceptions.RequestException:
                cached_path = _cached_chromedriver_path(driver_version)
                if cached_path is None:
                    raise
                driver_path = cached_path

            driver_path = _normalize_chromedriver_path(driver_path)
            service = ChromeService(driver_path)
            driver = WebDriverExtended(
                webdriver.Chrome(service=service, options=options),
                WebDriverListener(), config
            )
            return driver
        elif config["browser"] == "firefox":
            options = webdriver.FirefoxOptions()
            if config["headless_mode"] is True:
                options.headless = True
            service = FirefoxService(GeckoDriverManager().install())
            driver = WebDriverExtended(
                webdriver.Firefox(service=service, options=options),
                WebDriverListener(), config
            )
            return driver
        elif config["browser"] == "edge":
            from selenium.webdriver.edge.options import Options as EdgeOptions

            options = EdgeOptions()
            options.use_chromium = True
            if config["headless_mode"] is True:
                options.headless = True
            driver_path = EdgeChromiumDriverManager().install()
            service = EdgeService(driver_path)
            driver = WebDriverExtended(
                webdriver.Edge(service=service, options=options),
                WebDriverListener(), config
            )
            return driver
        raise Exception("Provide valid driver name")
