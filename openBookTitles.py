from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def read_books(filename):
    with open(filename, "r") as file:
        return [book.strip() for book in file.readlines()]

def search_book(driver, book_title):
    def open_page(url):
        driver.get(url)
        time.sleep(2)  # wait for the page to load

    def try_open_site(site):
        open_page(f"https://www.google.com/search?q={book_title}+{site}")
        try:
            link = driver.find_element_by_partial_link_text(site.capitalize())
            link.click()
            return True
        except:
            return False

    # Use Wikipedia first
    if not try_open_site("wikipedia"):
        # If not, use Goodreads
        if not try_open_site("goodreads"):
            # If neither exists, leave it at Google search results
            open_page(f"https://www.google.com/search?q={book_title}")

def open_new_tab(driver):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

def main():
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
