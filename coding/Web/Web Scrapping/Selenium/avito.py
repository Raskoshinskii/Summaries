from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time



PATH = 'C:\Program Files (x86)\chromedriver.exe'
URL = 'https://www.avito.ru/permskiy_kray'

def get_page_data(url = URL, path = PATH , item_name = 'iPhone 11'):
    # Page opening 
    browser = webdriver.Chrome(path)
    browser.get(url)
    # Inserting What We Are Looking For 
    search_field = browser.find_element_by_id('search')
    search_field.send_keys(item_name)
    search_field.send_keys(Keys.RETURN)

    try:
        target_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='items-items-38oUm']"))
        )
        
        all_items = target_element.find_elements_by_xpath("//span[@class='title-root-395AQ iva-item-title-1Rmmj title-list-1IIB_ title-root_maxHeight-3obWc text-text-1PdBw text-size-s-1PUdo text-bold-3R9dt']")
        for item in all_items[:7]:
            if item_name.lower() in item.text.lower():
                item.click()

                # For some reasons this elemen can't be found. May be there is a special protection (can be continued later)
                phone_element = WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[@class='js-item-phone-react']"))
                )s
                print(phone_element.text)

                time.sleep(10)
            
    finally:
        browser.quit()

"""
Some useful methods
1. webdriver.take_screenshot()
2. webdriver.location (x,y)
3. webdriver.size (width and height)
5. pip install pytesseract for characters and numbers recognition 
6. from pytesseract import image_to_string
"""

if __name__ == '__main__':
    get_page_data()