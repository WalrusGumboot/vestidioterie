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
    soup = BeautifulSoup(huis.get_attribute("innerHTML"), 'html.parser')
    titel = soup.find("h3", class_="house-thumb-title").text.strip()
    prijs = soup.find("div", class_="house-thumb-meta-price").text.splitlines()[2].strip()
    link  = f"https://rooms.vestide.nl{soup.find('a', class_='house-thumb-click-area').get('href')}"

    #print(soup.prettify())
    print(f"{titel} voor {prijs}; op {link}")