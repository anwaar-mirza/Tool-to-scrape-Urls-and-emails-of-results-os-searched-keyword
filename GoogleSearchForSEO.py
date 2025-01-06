import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver. common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from mailFinder import get_email_address, initialize_mail_driver
from threading import Thread
from fake_useragent import UserAgent
import pandas as pd
import time
import os


class SEOFinding:
    def __init__(self):
        # service = Service(ChromeDriverManager().install())
        options = Options()
        fake_agent = UserAgent()
        options.binary_location = "/usr/bin/chromium"
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"user-agent={fake_agent.chrome}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 3)
        self.action = ActionChains(self.driver)
        self.driver.get("https://www.google.com")
        self.driver.implicitly_wait(4)

    def search_keyword(self, key_to_search):
        try:
            input = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//textarea[@title="Search" or @class="gLFyf"]')))
            input.send_keys(key_to_search, Keys.ENTER)
            time.sleep(2)
            return self.driver.current_url.strip()
        except:
            print("Fail to Search")

    def target_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(3)

    def close_now(self):
        self.driver.close()

    
    def extract_links(self, path):
        try:
            links = [l.get_attribute('href') for l in self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@jsname="UWckNb"]')))]
            bot = initialize_mail_driver()    
            for i, l in enumerate(links, start=1):
                result = get_email_address(bot, l)
                print(str(i)+"----->"+str(result))
                res_dict = {
                    "Link": l,
                    "Email": result
                }
                p = pd.DataFrame([res_dict])
                p.to_csv(path, mode='a', header=not os.path.exists(path), index=False)
        except Exception as e:
            print(f"Fail to get links.....{e}")

    def go_down(self):
       self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       time.sleep(1)

    def get_total_pages(self):
        try:
            last_number = self.wait.until(EC.presence_of_element_located((By.XPATH, '//table[@class="AaVjTc"]//tr//td[last()-1]')))
            return last_number.text
        except:
            return None
        
    def click_on_next_button(self):
        try:
            next = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="oeN89d" and contains(text(), "Next")]')))
            self.action.click(next).perform()
        except:
            print("Fil to click on next button....")





def process_url(id, the_url):
    chat = the_url
    oq_position = chat.find("&oq=")
    if oq_position != -1:
        chat = chat[:oq_position] + f"&start={id}" + chat[oq_position:]
        return chat

def implement_threading(page, base_url, path):
    pu = process_url(page, base_url)
    bot = SEOFinding()
    bot.target_url(pu)
    bot.extract_links(path)
    bot.close_now()

def extract_seo(scrape_type, key_words, path):
    if scrape_type == "Single Keyword":
        bot = SEOFinding()
        res = bot.search_keyword(key_words)
        bot.go_down()
        last_page = bot.get_total_pages()
        bot.close_now()
        for i in range(0, (int(last_page)*10)+1, 10):
            th = Thread(target=implement_threading, args=[i, res, path])
            th.start()
            time.sleep(5)
        else:
            time.sleep(2)
    elif scrape_type == "By File":
        bot = SEOFinding()
        for k in key_words:
            res = bot.search_keyword(k)
            bot.go_down()
            last_page = bot.get_total_pages()
            bot.quit()
            for i in range(0, (int(last_page)*10)+1, 10):
                th = Thread(target=implement_threading, args=[i, res, path])
                th.start()
                time.sleep(5)
        else:
            time.sleep(2)

            
                

            

