from faker import Faker
from collections import OrderedDict
import pyautogui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
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

status = ''
amtdone = 0
def setstatus():
    global status
    while True:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleTitleW("Gmail Generator | " + status)

sthread = threading.Thread(target=setstatus)

sthread.start()

config= configparser.ConfigParser()
config.read(r'config.ini')
URL = config['CONFIG']['smsurl'].split(", ")

Proxies = []
def FillProxies():
    global totalnums
    with open('proxies.txt', "r") as file:
        for line in file:
            Proxies.append(line)
FillProxies()
CycleProxies = cycle(Proxies)

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

GlobalPassword = 'L@rgeB0l@s69*'
GmailURL = 'https://accounts.google.com/signup'
fake = Faker(locales)
totalnums = []
def GetPhoneNumbers():
    with open('TMAccounts.txt', "r") as file:
        for line in file:
            if ',' in line:
                values = line.strip().split(",")
                phone_number = values[4]
                if len(phone_number) == 11 and phone_number[:1] == '1':
                    phone_number = phone_number[1:]
                totalnums.append(phone_number)
            else:
                phone_number = line
                if len(phone_number) > 11 and phone_number[:1] == '1':
                    phone_number = phone_number[1:]
                totalnums.append(phone_number[:10])

    with open('PhoneNumbers.txt','w') as ph:
        for v in totalnums:
            ph.write(v + '\n')

def rwait():
    time.sleep(random.uniform(1, 3))

def startnew(prox):
    proxy = prox.split(':')
    optionss = {
    'proxy': {
        'http': f"http://{proxy[2]}:vj8gyk0x45wh@{proxy[0]}:{proxy[1]}",
        'https': f"https://{proxy[2]}:vj8gyk0x45wh@{proxy[0]}:{proxy[1]}",
        'no_proxy': 'localhost,127.0.0.1'
        }
    }
    # other chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')

    driver = webdriver.Chrome(options = chrome_options, seleniumwire_options=optionss)
    return driver

def click(element, driver):
    rwait()
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()

def type(element, text):
    rwait()
    if text:
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
    else:
        element.send_keys(text)

def filltotalnums():
    global totalnums
    with open('PhoneNumbers.txt', "r") as file:
        for line in file:
            totalnums.append(line)

filltotalnums()

badnums = []
def fillbadnums():
    global badnums
    with open('BadGmailNumbers.txt', "r") as file:
        for line in file:
            badnums.append(line)

fillbadnums()
cyclephones = cycle(totalnums)
print(f"Total of {len(totalnums)} phone numbers")
print(f"Total of bad {len(badnums)} phone numbers")

def enter_proxy_auth():
    time.sleep(1)
    print("entering proxy auth")
    pyautogui.typewrite('796172345f7277696c6465723036303140676d61696c2e636f6d2d636f756e7472792d75732d73657373696f6e2d6163663233')
    pyautogui.press('tab')
    pyautogui.typewrite('vj8gyk0x45wh')
    pyautogui.press('enter')

def GenGmails():
    global status
    global amtdone
    global cyclephones
    global badnums
    global CycleProxies
    NewProxy = next(CycleProxies)
    driver = startnew(NewProxy)
    wait = WebDriverWait(driver, 10)
    status = "Loading gmail"
    driver.get(GmailURL)
    #enter_proxy_auth()
    FakeFirst = fake.name().split()[0]
    FakeLast = fake.name().split()[1]
    CUserName = f"{FakeFirst}{FakeLast}{str(random.randint(1000, 99999))}"
    PhoneNumberRando = next(cyclephones)
    
    while PhoneNumberRando in badnums:
        time.sleep(0.1)
        print("Bad number found, skipping " + PhoneNumberRando[:10])
        PhoneNumberRando = next(cyclephones)

    PhoneNumberRandom = PhoneNumberRando[:10]

    print(f"Found good number {PhoneNumberRandom}")
    try:
        rwait()
        status = "Entering First Name"
        FirstName = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="firstName"]')))
        type(FirstName, FakeFirst)
        status = "Entering Last Name"
        LastName = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="lastName"]')))
        type(LastName, FakeLast)
        LastName.send_keys(Keys.ENTER)
        status = "Inputting Birthday"
        Month = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='month']")))
        Select(Month).select_by_value(str(random.randint(1, 12)))
        rwait()
        Day = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="day"]')))
        type(Day, str(random.randint(1, 27)))
        Year = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="year"]')))
        type(Year, str(random.randint(1970, 2001)))
        Gender = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='gender']")))
        Select(Gender).select_by_value(str(random.randint(1, 3)))
        rwait()
        Year.send_keys(Keys.ENTER)
        status = "Figuring out username"
        rwait()
        #Check which username page
        try:#
            check1 = driver.find_elements(By.XPATH, "//*[contains(text(), 'Choose your Gmail address')]")
            if len(check1) > 0:#Exists
                driver.execute_script("""document.evaluate("//*[contains(text(), 'Create your own Gmail address')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""")
                UName = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="Username"]')))
                type(UName, CUserName)
                UName.send_keys(Keys.ENTER)
            else:
                rwait()
                UName = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="Username"]')))
                type(UName, CUserName)
                UName.send_keys(Keys.ENTER)
        except Exception as er:
            print("Error creating email: " + str(er))
        status = "Entering Password"
        rwait()
        Password = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="Passwd"]')))
        type(Password, f"{GlobalPassword}")
        ConfirmPassword = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="PasswdAgain"]')))
        type(ConfirmPassword, f"{GlobalPassword}")
        ConfirmPassword.send_keys(Keys.ENTER)
        time.sleep(3)
        #Check if phone number is needed
        GotCode = False
        try:#
            status = "Entering phone number"
            check1 = driver.find_elements(By.XPATH, "//*[contains(text(), 'Get a verification code sent to your phone')]")
            if len(check1) > 0:#Exists
                PhoneNumber = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="phoneNumberId"]')))
                type(PhoneNumber, f"{PhoneNumberRandom}")
                PhoneNumber.send_keys(Keys.ENTER)
                time.sleep(5)
                status = "Finding verification code"
                VerificationCode = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="code"]')))
                code = GetCode(PhoneNumberRandom)
                type(VerificationCode, code)
                VerificationCode.send_keys(Keys.ENTER)
                GotCode = True
                status = "Found verification code: " + code
            else:
                driver.close()
                amtdone -=1
                return 0
        except Exception as er:
            print("Error with verification, retrying")
            with open("BadGmailNumbers.txt", "a") as file:
                file.write(PhoneNumberRandom + '\n')
            driver.close()
            amtdone -= 1
            return 0
        while not GotCode:#
            time.sleep(1)
        status = "Completing misc. tasks"
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Skip']")))
        driver.execute_script("""document.evaluate("//span[text()='Skip']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""")
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Add phone number']")))
        driver.execute_script("""document.evaluate("//span[text()='Skip']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""")
        rwait()
        anotherpg = driver.find_elements(By.XPATH, "//span[text()='Get more from your number']")
        if len(anotherpg) > 0:
            driver.execute_script("""document.evaluate("//span[text()='Skip']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""")

        wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Next']")))
        driver.execute_script("""document.evaluate("//span[text()='Next']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""")
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='I agree']")))
        driver.execute_script("""document.evaluate("//span[text()='I agree']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""")
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Confirm']")))
        driver.execute_script("""document.evaluate("//span[text()='Confirm']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""")
        wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'Welcome, {FakeFirst} {FakeLast}')]")))
        status = "Finished creating account"
        print(f"[{amtdone}] Account Generated: {CUserName}@gmail.com")
        with open('GeneratedAccounts.txt', 'a') as y:
            y.write(f"{CUserName}@gmail.com,{PhoneNumberRandom},{GlobalPassword}\n")
        driver.close()
    except Exception as ER:
        driver.save_screenshot("ERROR.png")
        print("Error, retrying")
        driver.close()
        amtdone -= 1
        return 0
#GetPhoneNumbers()
amtgen = input("How many accounts should be generated?\n")
amtgen = int(amtgen)
print("Generating " + str(amtgen) + " gmail accounts")
while amtdone < amtgen:
    amtdone +=1
    GenGmails()
    time.sleep(5)
input("Finished generating " + str(amtdone) + " accounts. Please check GeneratedAccounts.txt")
