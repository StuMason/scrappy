import os
import boto3
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Create an S3 client


class ChromeService:
    def __init__(self):
        self.driver = self._init_driver()
        self.client = boto3.client(
            "s3",
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
            endpoint_url="http://host.docker.internal:4566"
        )

    def _init_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options = self._configure_options(chrome_options)
        service = Service(executable_path="/opt/chromedriver")
        return webdriver.Chrome(service=service, options=chrome_options)

    def _configure_options(self, chrome_options):
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-dev-tools")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors'")
        chrome_options.add_argument("--page_load_strategy='normal'")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--no-cache")
        chrome_options.add_argument("--dns-prefetch-disable")
        chrome_options.add_argument("--window-size=1920x1920")

        chrome_options.binary_location = "/opt/chrome/chrome"
        return chrome_options

    def get_url(self, url):
        try:
            self.driver.get(url)
        except Exception:
            traceback.print_exc()

    def wait(self):
        try:
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except Exception:
            traceback.print_exc()

    def wait_by_class(self, class_name):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
        except Exception:
            traceback.print_exc()

    def wait_till_gone_by_class(self, class_name):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, class_name))
            )
        except Exception:
            traceback.print_exc()

    def click_by_id(self, element_id):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.ID, element_id))
            ).click()
        except Exception:
            traceback.print_exc()

    def click_by_xpath(self, xpath):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            ).click()
        except Exception:
            traceback.print_exc()

    def screenshot(self, name):
        try:
            self.driver.save_screenshot(f"/tmp/{name}.png")
            self.client.upload_file(
                f"/tmp/{name}.png",
                'test',
                f"{name}.png",
            )
            print(f"saved screenshot for {name}")
        except Exception:
            traceback.print_exc()

    def click_by_class(self, class_name):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            ).click()
        except Exception:
            traceback.print_exc()

    def click_by_class_where_content(self, class_name, content):
        try:
            calendar = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.c-pane-container"))
            )
            dates = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.c-day-content"))
            )
            for date in dates:
                if date.text == content:
                    date.click()
                    break
        except Exception:
            traceback.print_exc()

    def get_loaded_source(self):
        try:
            return self.driver.page_source
        except Exception:
            traceback.print_exc()

    def wait_for_class(self, class_name):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
        except Exception:
            traceback.print_exc()
            
    def is_text_visible(self, text):
        try:
            if WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//*[contains(text(), '{text}')]")
                )
            ):
                return True
            return False
        except TimeoutException:
            return False
        except Exception:
            traceback.print_exc()

    def close(self):
        self.driver.quit()
