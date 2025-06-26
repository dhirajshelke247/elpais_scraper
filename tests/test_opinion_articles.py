from pages.home_page import HomePage
from pages.opinion_page import OpinionPage
from collections import Counter
import re

import pytest

def test_scrape_and_translate(driver_config, driver, base_url):
    driver.get(base_url)
    home = HomePage(driver)
    home.accept_consent()
    assert home.is_in_spanish()

    home.go_to_opinion()

    opinion = OpinionPage(driver)
    results, translated_titles = opinion.get_articles()

    for article in results:
        print("\n--- Article ---")
        print("Title:", article["title"])
        print("Translated:", article["translated_title"])
        print("Summary:", article["summary"])
        print("Image saved at:", article["img_path"])

    words = []
    for title in translated_titles:
        title = re.sub(r"[^\w\s]", "", title.lower())
        words.extend(title.split())

    counter = Counter(words)
    for word, count in counter.items():
        if count > 2:
            print(f'Word "{word}" repeated {count} times')
