import os
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ChromeService:
    def __init__(self):
        self.driver = self._init_driver()

    def _init_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options = self._configure_options(chrome_options)
        service = Service(executable_path="/opt/chromedriver")
        return webdriver.Chrome(service=service, options=chrome_options)

    def _configure_options(self, chrome_options):
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-dev-tools")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--ignore-certificate-errors'")
        chrome_options.add_argument("--page_load_strategy='normal'")
        chrome_options.binary_location = "/opt/chrome/chrome"
        return chrome_options

    def get_url(self, url):
        try:
            self.driver.get(url)
        except Exception:
            traceback.print_exc()

    def get_loaded_source(self):
        try:
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            return self.driver
        except Exception:
            traceback.print_exc()

    def click_privacy_and_wait(self):
        try:
            privacy_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-role="b_agree"]'))
            )
            if privacy_button:
                privacy_button.click()

                WebDriverWait(self.driver, 30).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
            return self.driver
        except Exception:
            traceback.print_exc()

    def find_by_xpath(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def get_page_source(self):
        return self.driver.page_source

    def close(self):
        self.driver.quit()
