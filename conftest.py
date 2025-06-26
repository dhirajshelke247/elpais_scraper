import os
import json
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from dotenv import load_dotenv 

load_dotenv()  

def load_browserstack_config():
    with open("browserstack/browserstack_config.json") as f:
        return json.load(f)["browsers"]

def get_browserstack_driver(config):
    from selenium.webdriver import ChromeOptions, FirefoxOptions, SafariOptions, EdgeOptions

    caps = config.copy()
    caps["browserstack.user"] = os.getenv("BROWSERSTACK_USERNAME")
    caps["browserstack.key"] = os.getenv("BROWSERSTACK_ACCESS_KEY")
    caps["name"] = "ElPais Article Test"

    browser_name = caps.get("browser", "").lower()
    if "chrome" in browser_name:
        options = ChromeOptions()
    elif "firefox" in browser_name:
        options = FirefoxOptions()
    elif "edge" in browser_name:
        options = EdgeOptions()
    else:
        options = SafariOptions()

    for key, value in caps.items():
        options.set_capability(key, value)

    return WebDriver(
        command_executor="https://hub-cloud.browserstack.com/wd/hub",
        options=options
    )


def pytest_generate_tests(metafunc):
    if "driver_config" in metafunc.fixturenames:
        configs = load_browserstack_config()
        metafunc.parametrize("driver_config", configs)

@pytest.fixture(scope="function")
def driver(driver_config):
    driver = get_browserstack_driver(driver_config)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")
