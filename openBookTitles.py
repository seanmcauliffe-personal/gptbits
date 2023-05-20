"""
Module Docstring:
A module that opens a new browser tab for each book in a list, 
searching for information about the book on Wikipedia, Goodreads, or Google.
"""

import time
from selenium import webdriver

def read_books(filename):
    """
    Reads book titles from a file.
    :param filename: The name of the file.
    :return: A list of book titles.
    """
    with open(filename, "r", encoding='utf-8') as file:
        return [book.strip() for book in file.readlines()]

def search_book(driver, book_title):
    """
    Searches for a book on Wikipedia, Goodreads, or Google.
    :param driver: The webdriver instance.
    :param book_title: The title of the book.
    """
    def open_page(url):
        driver.get(url)
        time.sleep(2)  # wait for the page to load

    def try_open_site(site):
        open_page(f"https://www.google.com/search?q={book_title}+{site}")
        try:
            link = driver.find_element_by_partial_link_text(site.capitalize())
            link.click()
            return True
        except Exception:  # specify the general exception
            return False

    # Use Wikipedia first
    if not try_open_site("wikipedia"):
        # If not, use Goodreads
        if not try_open_site("goodreads"):
            # If neither exists, leave it at Google search results
            open_page(f"https://www.google.com/search?q={book_title}")

def open_new_tab(driver):
    """
    Opens a new tab and switches to it.
    :param driver: The webdriver instance.
    """
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

def main():
    """
    Main function that reads book titles from a file and opens a new tab for each book.
    """
    # Create a new instance of the Edge/Chrome driver
    driver = webdriver.Edge()  # or webdriver.Chrome()

    books = read_books("book_list.txt")

    for book in books:
        open_new_tab(driver)
        search_book(driver, book)

    # Switch back to the first tab
    driver.switch_to.window(driver.window_handles[0])

if __name__ == "__main__":
    main()
