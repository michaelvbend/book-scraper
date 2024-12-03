# Web Scraper for Book Data

This project is a web scraper designed to extract book data from a specified website. The scraper uses Selenium to navigate the website, locate book details, and save the extracted data into a JSON file.

## Features

- Extracts book details such as title, thumbnail, author, published date, description, page count, genre, and language.
- Handles cookies and navigation through multiple pages.
- Saves the extracted data incrementally to avoid data loss in case of interruptions.

## Requirements

- Python 3.x
- Selenium
- Chrome WebDriver

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/michaelvbend/book-scraper.git
   cd webscraper
   ```
2. **Install Python packages:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run the scraper**
   ```sh
   python main.py
   ```
2. **Output: The scraped data will be saved in book_data.json**
