import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from utils.translate_api import translate_text
from utils.download_image import download_image

class OpinionPage(BasePage):
    article_selector = (By.CSS_SELECTOR, "article.c.c-d")

    def get_articles(self, max_articles=5, download_dir="downloaded_images"):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.article_selector)
        )
        articles = self.driver.find_elements(*self.article_selector)[:max_articles]

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        results = []
        translated_titles = []

        for i, article in enumerate(articles):
            title_elem = article.find_element(By.CSS_SELECTOR, "h2.c_t a")
            title = title_elem.text
            url = title_elem.get_attribute("href")
            translated = translate_text(title)
            translated_titles.append(translated)

            try:
                summary = article.find_element(By.CSS_SELECTOR, "p.c_d").text
            except:
                summary = ""

            try:
                img_elem = article.find_element(By.CSS_SELECTOR, "img")
                img_url = img_elem.get_attribute("src")
                img_path = download_image(img_url, download_dir, f"article_{i+1}.jpg")
            except:
                img_url = img_path = None

            results.append({
                "title": title,
                "translated_title": translated,
                "url": url,
                "summary": summary,
                "img_url": img_url,
                "img_path": img_path
            })

        return results, translated_titles
