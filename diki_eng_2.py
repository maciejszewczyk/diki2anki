from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import re
import csv
import random


# -----------------------------
# Sentence extraction function
# -----------------------------
def extract_example_sentences(html: str):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for example in soup.find_all("div", class_="exampleSentence"):
        english_parts = [
            t.strip()
            for t in example.find_all(string=True, recursive=False)
            if t.strip()
        ]
        english = " ".join(english_parts)

        translation_span = example.find("span", class_="exampleSentenceTranslation")
        translation = ""
        if translation_span:
            translation = translation_span.get_text(strip=True)
            translation = re.sub(r"^\(|\)$", "", translation)

        if english and translation:
            results.append((english, translation))

    return results


# -----------------------------
# Read words
# -----------------------------
def read_words_from_file(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return [line.strip() for line in f if line.strip()]


# -----------------------------
# Crawl with real browser
# -----------------------------
def crawl_diki(words):
    base_url = "https://www.diki.pl/slownik-angielskiego?q="

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        with open("sentences.csv", "a", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")

            for word in words:
                url = base_url + word
                print(f"\nFetching: {url}")

                try:
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    html = page.content()
                    sentences = extract_example_sentences(html)

                    if not sentences:
                        print("  No example sentences found.")
                    else:
                        for en, tr in sentences:
                            writer.writerow([word, tr, en])

                    csv_file.flush()  # crash-safe

                except Exception as e:
                    print(f"  Error for '{word}': {e}")

                time.sleep(random.uniform(0.5, 1.5))  # polite crawling

        browser.close()


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    words = read_words_from_file("words.txt")
    crawl_diki(words)
