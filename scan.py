from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup


# start by defining the options
options = webdriver.ChromeOptions()
options.page_load_strategy = 'none'
options.add_argument('--headless')
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
driver = Chrome(options=options, service=chrome_service)

driver.get("https://rooms.vestide.nl/nl/vind-je-kamer/")
driver.implicitly_wait(10)
huizen = driver.find_elements(By.XPATH, "//div/article")

for huis in huizen:
    print("nieuw huis:")
    soup = BeautifulSoup(huis.get_attribute("innerHTML"), 'html.parser')
    titel = soup.find("h3", class_="house-thumb-title")
    prijs = soup.find("div", class_="house-thumb-meta-price")
