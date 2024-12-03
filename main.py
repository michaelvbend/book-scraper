from dataclasses import asdict, dataclass
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from variables import SITE_TO_SCRAPE, site_paths
import time

@dataclass
class Book:
    title: str
    thumbnail: str
    author: str
    published_date: str
    description: str
    page_count: str
    genre: str
    language: str    

def main():
    amount_of_pages = 500
    books_on_pages = 30
    page_number = 1
    scraped_books = 0
    dict_of_books = {
        "books": []
    }
    exception_list = []

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(SITE_TO_SCRAPE)
    
    # Cookies
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, site_paths.get('accept_button')))
    )
    accept_button.click()

    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, site_paths.get('continue_button')))
    )
    continue_button.click()    
    
    def scrapeBook(link):
        try:
            driver.get(link)
            script_tag = driver.find_element(By.XPATH, "//script[@type='application/ld+json']")
            json_content = script_tag.get_attribute('innerHTML')
            data = json.loads(json_content)

            description = data.get('description')
            title = data.get('name')
            author = data.get('author', {}).get('name')
            thumbnail = data.get('image', {}).get('url')
            published_date = data.get('workExample', [{}])[0].get('datePublished')
            page_count = data.get('workExample', [{}])[0].get('numberOfPages', '0')
            genre = data.get('genre', [])
            language = data.get('inLanguage')
            book = Book(title=title, thumbnail=thumbnail, description=description, author=author, published_date=published_date, page_count=page_count, 
                        genre=genre, language=language)
            print(f"Title: {title}")
            return book
        except Exception as e:
            print(e)
    # Actual scraping of the book data
    with open("book_data.json", "a", encoding='utf-8') as outfile:
        while page_number < amount_of_pages:
            driver.get(f'{SITE_TO_SCRAPE}?page={page_number}')
            elements = driver.find_elements(By.XPATH, site_paths.get('books_on_page'))
            list_of_hrefs = [element.get_attribute('href') for element in elements]
            for link in list_of_hrefs:
                try:
                    book = scrapeBook(link)
                    json.dump(asdict(book), outfile, ensure_ascii=False, indent=4)
                    outfile.write('\n') 
                except Exception as e:
                    continue
            scraped_books = scraped_books + (page_number * books_on_pages)
            print(f"Bookcount: {scraped_books}")
            time.sleep(5)
            page_number += 1
    driver.quit()

if __name__ == "__main__":
    main()