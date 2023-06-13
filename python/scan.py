from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
from time import sleep
import os

from pyfcm import FCMNotification

import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("creds.json")
firebase_admin.initialize_app(cred)

# start by defining the options
options = webdriver.ChromeOptions()
options.page_load_strategy = 'none'
options.add_argument('--headless')
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
driver = Chrome(options=options, service=chrome_service)

def gen_file():
    driver.get("https://rooms.vestide.nl/nl/vind-je-kamer/")
    driver.implicitly_wait(10)
    huizen = driver.find_elements(By.XPATH, "//div/article")
    with open("new.txt", "w") as newfile:
        for huis in huizen:
            soup = BeautifulSoup(huis.get_attribute("innerHTML"), 'html.parser')
            titel = soup.find("h3", class_="house-thumb-title").text.strip()
            prijs = soup.find("div", class_="house-thumb-meta-price").text.splitlines()[2].strip()
            link  = f"https://rooms.vestide.nl{soup.find('a', class_='house-thumb-click-area').get('href')}"

            #print(soup.prettify())
            print(f"huis gevonden: {titel}")
            newfile.write(f"{titel} voor {prijs} op {link}\n")


iterations = 0
while True:
    iterations += 1
    print(f"beginnen aan iteratie {iterations}")
    old = []
    with open("new.txt", "r") as f:
        old = [x.strip() for x in f.readlines()]
    oldSet = set(old)

    print(f"eerder: {oldSet}")

    os.system("rm new.txt")

    gen_file()


    new = []
    with open("new.txt", "r") as f:
        new = [x.strip() for x in f.readlines()]
    newSet = set(new)

    print(f"later: {newSet}")
    diff = newSet.difference(oldSet)

    print(f"er zijn {len(diff)} nieuwe huizen gevonden.")

    for nieuwHuis in diff:
        print(f"  gevonden: {nieuwHuis}")
        bericht = messaging.Message(topic="woning",notification=messaging.Notification(title="Er is een nieuwe woning beschikbaar!", body=f"De Vestidioterie-app heeft een nieuwe woning gedetecteerd: {nieuwHuis}"))
        result = messaging.send(bericht)
    sleep(120)
