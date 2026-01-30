from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from models import *


def get_part_URL(appliance, part_ID):
    print("ENTERING PART URL")
    """
    Docstring for get_part_URL
    
    :param appliance: Description
    :param part_ID: Description

    Find the URL for a given <part_ID> of appliance type <appliance>
    """
    if appliance == "Refrigerator": APPL_ROOT = "Refrigerator-Parts"
    else: APPL_ROOT = "Dryer-Parts"
    URL = f"https://www.partselect.com/{APPL_ROOT}.htm"
    
    try:
        driver = webdriver.Chrome()
        driver.get(URL)
        search = driver.find_element(By.ID, "searchboxInput")
        search.clear()
        search.send_keys(part_ID)
        search.send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(lambda d: d.current_url != URL)
        return driver.current_url
    except:
        return False

def get_part_information(appliance, part_ID):
    print("ENTERING PART INFO")
    """
    Docstring for get_part_information
    
    :param appliance: Description
    :param part_ID: Description

    Get information for a given <part_ID> of appliance type <appliance>

    Information includes
    * Name
    * Product Description
    * Installation Instructions
    * Troubleshooting Instructions
    * Relevent instructional youtube videos
    * Price
    """
    URL = get_part_URL(appliance, part_ID)
    try:
        driver = webdriver.Chrome()
        driver.get(URL)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )


        part_information = {}
        part_information['name'] = driver.find_element(By.TAG_NAME, "h1").text
        part_information['price'] = driver.find_element(By.CSS_SELECTOR, "span.price.pd__price").text
        desc = driver.find_element(By.CSS_SELECTOR, "div.pd__wrap")
        part_information['description_html'] = desc.get_attribute("innerHTML")
        part_information['troubleshooting_html'] = driver.find_element(By.CSS_SELECTOR, "div.pd__wrap").get_attribute("innerHTML")
        videos = driver.find_elements(By.CSS_SELECTOR, "div.yt-video")
        part_information['yt_urls'] = list(set([
            f"https://www.youtube.com/watch?v={v.get_attribute('data-yt-init')}"
            for v in videos
        ]))

        driver.quit()

        return part_information
    except:
        return False