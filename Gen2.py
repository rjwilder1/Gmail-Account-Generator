from faker import Faker
from collections import OrderedDict
from playwright.sync_api import BrowserContext, sync_playwright
from undetected_playwright import stealth_sync
from bs4 import BeautifulSoup
import requests
import time
import random
import configparser
import threading
import ctypes
from itertools import cycle
locales = OrderedDict([
    ('en-US', 1)
])
amtdone = 0
config= configparser.ConfigParser()
config.read(r'config.ini')
URL = config['CONFIG']['smsurl'].split(", ")
GlobalPassword = 'L@rgeB0l@s69*'
fake = Faker(locales)
totalnums = []
badnums = []
amtdone = 0
def filltotalnums():
    global totalnums
    with open('PhoneNumbers.txt', "r") as file:
        for line in file:
            totalnums.append(line)

def fillbadnums():
    global badnums
    with open('BadGmailNumbers.txt', "r") as file:
        for line in file:
            badnums.append(line)

fillbadnums()
filltotalnums()

cyclephones = cycle(totalnums)

def GetCode(PhoneNum):
    global URL
    FoundNumber = False
    while not FoundNumber:
        time.sleep(1)
        for SMSURL in URL:
            response = requests.get(SMSURL)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            table = soup.find('table')
            if table:
                msgs = table.find_all('tr')
                if len(msgs) >= 1:
                    td_elements = msgs[0].find_all('td')
                    if len(td_elements) >= 3:
                        PhoneNumber = td_elements[0].get_text()
                        if PhoneNum in PhoneNumber:
                            Code1 = td_elements[2].get_text() 
                            c = Code1.split()
                            VCode = c[0]
                            Code = VCode[2:]
                            FoundNumber = True
                            return Code
            if FoundNumber:
                break

def rwait():
    time.sleep(random.uniform(1, 3))

def run(context: BrowserContext):
    FakeFirst = fake.name().split()[0]
    FakeLast = fake.name().split()[1]
    CUserName = f"{FakeFirst}{FakeLast}{str(random.randint(1000, 99999))}"
    PhoneNumberRando = next(cyclephones)
    while PhoneNumberRando in badnums:
        time.sleep(0.1)
        PhoneNumberRando = next(cyclephones)
    PhoneNumberRandom = PhoneNumberRando[:10]
    page = context.new_page()
    page.goto("https://accounts.google.com/")
    page.get_by_role("button", name="Create account").click()
    page.get_by_text("For my personal use").click()
    page.get_by_role("textbox", name="First name").fill(FakeFirst)
    page.get_by_role("textbox", name="Last name (optional)").fill(FakeLast)
    page.get_by_role("button", name="Next").click()
    page.get_by_role("combobox", name="Month").select_option(str(random.randint(1, 12)))
    page.get_by_role("textbox", name="Day").fill(str(random.randint(1, 27)))
    page.get_by_role("textbox", name="Year").fill(str(random.randint(1970, 2001)))
    page.get_by_role("combobox", name="Gender").select_option(str(random.randint(1, 3)))
    rwait()
    page.get_by_role("button", name="Next").click()
    rwait()
    if page.query_selector("text=Create your own Gmail address"):
        page.query_selector("text=Create your own Gmail address").click()
        rwait()
        page.locator("xpath=//input[@name='Username']").fill(CUserName)
        rwait()
    else:
        page.get_by_role("textbox", name="Username").fill(CUserName)
        rwait()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Password").fill(GlobalPassword)
    page.get_by_role("textbox", name="Confirm").fill(GlobalPassword)
    rwait()
    page.get_by_role("button", name="Next").click()
    page.get_by_label("Phone number").fill(PhoneNumberRandom)
    rwait()
    page.get_by_role("button", name="Next").click()
    GoodNumber = False
    rwait()
    while GoodNumber == False:
        if page.query_selector("text=used too many") is None:
            GoodNumber = True
            break
        else:
            with open("BadGmailNumbers.txt", "a") as file:
                file.write(f"{PhoneNumberRandom}\n")
            
            badnums.append(PhoneNumberRandom)
            PhoneNumberRandom = next(cyclephones)[:10]
            if PhoneNumberRandom not in badnums:
                page.get_by_label("Phone number").fill(PhoneNumberRandom)
                rwait()
                page.get_by_role("button", name="Next").click()
        time.sleep(1)

    code = GetCode(PhoneNumberRandom)
    page.get_by_role("textbox", name="Enter code").fill(code)
    rwait()
    page.get_by_role("button", name="Next").click()
    rwait()
    page.get_by_role("button", name="Skip").click()
    rwait()
    page.get_by_role("button", name="Skip").click()
    rwait()
    page.get_by_role("button", name="Next").click()
    rwait()
    page.get_by_role("button", name="I agree").click()
    rwait()
    page.get_by_role("button", name="Confirm").click()
    rwait()
    page.wait_for_url("https://myaccount.google.com/?pli=1")

    print(f"[{amtdone}] Account Generated: {CUserName}@gmail.com")
    with open('GeneratedAccounts.txt', 'a') as y:
        y.write(f"{CUserName}@gmail.com,{PhoneNumberRandom},{GlobalPassword}\n")

amtgen = input("How many accounts should be generated?\n")
amtgen = int(amtgen)
print("Generating " + str(amtgen) + " gmail accounts")
while amtdone < amtgen:
    amtdone +=1
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, proxy={"server": "http://brd.superproxy.io:22225", "username": "brd-customer-hl_248f1d98-zone-isp", "password": "949guyouxe7i"})
        context = browser.new_context()
        stealth_sync(context)
        run(context)
        context.close()
        browser.close()
    time.sleep(5)

input("Finished generating " + str(amtdone) + " accounts. Please check GeneratedAccounts.txt")