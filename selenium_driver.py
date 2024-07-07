from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


def get_random_user_agent():
    ua = UserAgent()
    return ua.random


def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    mobile_emulation = {
        "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
        "userAgent": get_random_user_agent()
    }

    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(options=chrome_options)
    return driver
