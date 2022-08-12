from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import easygui
from configparser import ConfigParser
import logging


class ReviewClicker:
    def __init__(self):
        self.config = ConfigParser()
        logging.info("Loading config")

        self.config.read("config.ini")

        self.url = self.config.get("NearCrowd", "url")
        self.sunshine_button_xpath = self.config.get(
            "NearCrowd", "sunshine_button_xpath"
        )
        self.sunshine_review_button_xpath = self.config.get(
            "NearCrowd", "sunshine_review_button_xpath"
        )
        self.sunshine_header_xpath = self.config.get(
            "NearCrowd", "sunshine_header_xpath"
        )

        self.user_data_dir = self.config.get("ChromeProfile", "user_data_dir")
        self.profile_directory = self.config.get("ChromeProfile", "profile_directory")

        self.options = Options()
        self.options.add_argument(f"--profile-directory={self.profile_directory}")
        self.options.add_argument(f"user-data-dir={self.user_data_dir}")
        self.options.add_argument("--headless")

        self.driver = self.init_chrome()

    def init_chrome(self):
        logging.info("Starting Chrome")

        driver = webdriver.Chrome(options=self.options)

        return driver

    def load_page(self):
        logging.info("Opening page")

        self.driver.get(self.url)

        logging.info("Waiting for page to load")

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"{self.sunshine_button_xpath}"))
        )

        logging.info("Found the taskset")

        self.driver.find_element(By.XPATH, f"{self.sunshine_button_xpath}").click()

        logging.info("Taskset opened")
        logging.info("Waiting for page to load")

    def click_review_button(self):
        logging.info("Looking for review button")

        review_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"{self.sunshine_review_button_xpath}")
            )
        )

        logging.info("Found review button")

        if review_button:
            self.driver.find_element(
                By.XPATH, f"{self.sunshine_review_button_xpath} "
            ).click()

        logging.info("Review button clicked")

    @staticmethod
    def pop_up():
        return easygui.msgbox("Review found", "Alert", ok_button="OK")

    def find_review(self):
        while WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"{self.sunshine_header_xpath}"))
        ):

            self.click_review_button()

            try:
                WebDriverWait(self.driver, 3).until(
                    EC.alert_is_present(), "Timed out waiting for alert"
                )

                alert = self.driver.switch_to.alert
                alert.accept()

                logging.info("Alert accepted")
            except TimeoutException:
                self.pop_up()
                logging.info("Review found")

                return

        return


def main():
    logging.basicConfig(level=logging.INFO)

    review_clicker = ReviewClicker()

    review_clicker.load_page()
    # review_clicker.find_review()


if __name__ == "__main__":
    main()
