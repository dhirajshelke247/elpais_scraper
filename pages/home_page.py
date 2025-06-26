from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class HomePage(BasePage):
    consent_button = (By.ID, 'didomi-notice-agree-button')
    hamburger_button = (By.ID, "btn_open_hamburger")
    language_xpath_mobile = (By.XPATH, '//*[@id="hamburger_container"]/div[3]/div/ul/li[2]/a/span')
    language_xpath_desktop = (By.XPATH, '//li[@id="edition_head"]//span')
    opinion_link = (By.XPATH, '//a[contains(@href, "/opinion/") and contains(text(), "Opinión")]')

    def __init__(self, driver, driver_config=None):
        super().__init__(driver)
        self.driver_config = driver_config or {}

    def is_mobile(self):
        return bool(self.driver_config.get("real_mobile") or self.driver_config.get("device"))

    def accept_consent(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.consent_button)
            ).click()
            print("[i] Clicked standard consent button.")
        except:
            try:
                ios_consent_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pmConsentWall-button'))
                )
                ios_consent_button.click()
                print("[i] Clicked iOS-specific consent button.")
            except Exception as e:
                print(f"[!] Consent button not found or not clickable: {e}")

    def click_hamburger_if_mobile(self):
        if self.is_mobile():
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.hamburger_button)
                ).click()
            except Exception as e:
                print(f"[!] Could not click hamburger menu: {e}")

    def is_in_spanish(self):
        try:
            xpath = self.language_xpath_mobile if self.is_mobile() else self.language_xpath_desktop
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(xpath)
            )
            return elem.text.lower().startswith("es")
        except:
            return False

    def go_to_opinion(self):
        if self.is_mobile():
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.hamburger_button)
                ).click()
            except Exception as e:
                print(f"[!] Could not click hamburger menu: {e}")

        try:
            opinion_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//a[contains(@href, "/opinion/") and contains(text(), "Opinión")]'
                ))
            )

            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((
                        By.XPATH, '//a[contains(@href, "/opinion/") and contains(text(), "Opinión")]'
                    ))
                ).click()
            except:
                self.driver.execute_script("arguments[0].click();", opinion_link)

        except Exception as e:
            print(f"[!] Failed to click Opinión link: {e}")

