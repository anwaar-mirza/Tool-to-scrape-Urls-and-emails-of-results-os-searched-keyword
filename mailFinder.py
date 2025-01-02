from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.support.expected_conditions as EC
import time
import pickle
import requests
import re
class EmailFinder:
    def __init__(self):
        options = Options()
        service = Service(ChromeDriverManager().install())
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://www.facebook.com")
        with open("face_cook.pkl", "rb") as file: 
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.wait = WebDriverWait(self.driver, 5)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def extract_emails_from_requests(self, website_url):
        try:
            response = requests.get(website_url, timeout=10, headers=self.headers, allow_redirects=True)
            response.raise_for_status()
            raw_emails= re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", response.text)
            valid_emails = [
            email for email in raw_emails
            if not email.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.webpack')) and "wixpress.com" not in email and "sentry.io" not in email
            ]
            return valid_emails
        except requests.exceptions.RequestException as e:
            return []
        
    def extract_facebook_using_selenium(self, website_url):
        try:
            self.driver.get(website_url)
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            for l in links:
                if "facebook.com" in l.get_attribute('href'):
                    return l.get_attribute('href')
        except:
            pass
            

    def extract_emails_from_selenium(self, website_url):
        try:
            self.driver.get(website_url)
            all_links = self.driver.find_elements(By.XPATH, '//a[contains(@href, "mailto:") and contains(@href, "@")]')
            emails = [l.get_attribute('href') for l in all_links]
            return emails
        except Exception as e:
            return []

    def extract_emails_from_bs4(self, website_url):
        try:
            response = requests.get(website_url, timeout=10, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()
            return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text_content)
        except requests.exceptions.RequestException as e:
            return []
        
    def extract_email_from_facebook(self, facebook_url):
        try:
            self.driver.get(facebook_url)
            self.driver.implicitly_wait(3)
            body = self.driver.find_element(By.XPATH, "//h1").click()
            time.sleep(0.5)
            mail = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="xu06os2 x1ok221b"]/span[contains(text(), "@") and contains(text(), ".")]')))
            mail = [m.text for m in mail]
            return mail
        except:
            try:
                mail = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="xu06os2 x1ok221b"]/span[contains(text(), "@") and contains(text(), ".")]')))
                mail = [m.text for m in mail]
                return mail
            except Exception as e:
                return []



    def extract_emails(self, website_url):
        emails = self.extract_emails_from_requests(website_url)
        if emails:
            return emails

        emails = self.extract_emails_from_selenium(website_url)
        if emails:
            return emails

        return []


def initialize_mail_driver():
    return EmailFinder()

def get_email_address(bot, url):
    emails = bot.extract_emails(url)
    if len(emails) == 0:
        facebook = bot.extract_facebook_using_selenium(url)
        if facebook and facebook is not None:
            fb_email = bot.extract_email_from_facebook(facebook)
            return ", ".join(fb_email)
        else:
            return None
    else:
        final_mail = list(set(emails))
        final_mail = ", ".join(final_mail)
        return final_mail
