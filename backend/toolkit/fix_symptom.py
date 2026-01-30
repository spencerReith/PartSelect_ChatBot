import os
from pydantic_ai import Agent

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from models import *
from agents.symptom_recognizer import *

from config import model


def get_fix_for_problem(problem, machine_ID):
    print("ENTERING SYMPTOM BY URL")
    """
    Docstring for get_fixes_by_symptom_url
    
    :param URL: Description

    Get all fixes for a given symptom, specified by the symptom URL <URL>.
    You will need to find all potential symptoms using tool 'get_symptoms_by_machine_ID(machine_ID)', and then determine based on the user's problem which symptom they are experience.
    Then, you can use the URL returned by 'get_symptoms_by_machine_ID(machine_ID)' to call this tool.

    The tool returns a list of fixes, where each element is a dictionary that contains
    * 'percent': The percent chance this fix remedy's the symptom
    * 'name': The name of the part that could fix the symptom
    * 'part_ID': The part_ID for said part
    * 'price': The price of the part
    * 'img_url': URL for the image of the part
    """

    symptom = recognize_symptom(problem, "refrigerator")

    URL = f"https://www.partselect.com/Models/{machine_ID}/Symptoms/{symptom}/"
    print(URL)

    try:
        driver = webdriver.Chrome()
        driver.get(URL)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        fixes = []

        cards = driver.find_elements(By.CSS_SELECTOR, "div.symptoms.align-items-center")
        print(cards)
        print(len(cards))
        for card in cards:
            print('c')
            fix = {}
            fix['percent'] = card.find_element(By.CSS_SELECTOR, "div.symptoms__percent span").text
            fix['name'] = card.find_element(By.CSS_SELECTOR, "a.bold").text
            fix['part_ID'] = card.find_element(
                By.XPATH, ".//div[contains(text(),'Part Number')]/a"
            ).text
            fix['price'] = card.find_element(By.CSS_SELECTOR, "div.mega-m__part__price").text
            img = card.find_element(By.CSS_SELECTOR, "img")
            fix['img_url'] = img.get_attribute("src")

            fixes.append(fix)

        driver.quit()
        print('here')
    except:
        pass

    return fixes
