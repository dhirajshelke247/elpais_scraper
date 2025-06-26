from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class HomePage(BasePage):
    language_indicator = (By.XPATH, '//li[@id="edition_head" and @data-edition="el-pais"]//span[text()="España"]')
    articles_menu = (By.CSS_SELECTOR, 'a[href*="/opinion/"]')
    consent_button = (By.ID, 'didomi-notice-agree-button')

    def is_in_spanish(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@id="edition_head"]//span'))
        )
        return elem.text.lower().startswith("es")

    def accept_consent(self):
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.consent_button)
            )
            button.click()
        except:
            pass

    def go_to_opinion(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.articles_menu)
        )
        elem.click()
