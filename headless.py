from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

class Browser:
    def __init__(self):
        self.driver = webdriver.Firefox()
    
    def close(self):
        self.driver.close()
    
    def goto(self, url: str):
        self.driver.get(url)
    
    def find_el_xpath(self, xpath: str):
        return self.driver.find_element_by_xpath(xpath)
    
    def find_els_xpath(self, xpath: str):
        return self.driver.find_elements_by_xpath(xpath)

    def wait(self, el):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, el)))
    
    def press_enter(self, el):
        el.send_keys(Keys.ENTER)
    
    def scroll_bottom(self):
        SCROLL_PAUSE_TIME = 0.5
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height