from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from helpers.webdriver_listener import WebDriverListener
from extensions.webdriver_extended import WebDriverExtended


class DriverFactory:
    @staticmethod
    def get_driver(config) -> WebDriverExtended:
        if config["browser"] == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("start-maximized")
            if config["headless_mode"] is True:
                options.add_argument("--headless")
            service = ChromeService(ChromeDriverManager().install())
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
