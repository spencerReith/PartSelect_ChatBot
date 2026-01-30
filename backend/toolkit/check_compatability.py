import os
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai import Agent, Tool
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from models import *

##########################################
# CHECK COMPATABILITY
##########################################
def check_compatability(machine_ID, part_ID):
    print("ENTERING COMPATABILITY")
    """
    Docstring for check_compatability
    
    :param machine_ID: Description
    :param part_ID: Description

    Check if part <part_ID> is compatible with machine <machine_ID>
    """
    URL = f"https://www.partselect.com/Models/{machine_ID}/Parts/?SearchTerm={part_ID}"
    FAILURE_STATEMENT = "Failure in checking compatability between machine_ID and part_ID. Are both numbers definitely correct?"
    
    try:
        driver = webdriver.Chrome()
        driver.get(URL)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        results = driver.find_element(By.CSS_SELECTOR, "div.row.mt-3.align-items-stretch")
        exists = bool(len(results.find_elements(By.XPATH, "./*")) > 0)
        driver.quit()

        return exists
    except:
        return FAILURE_STATEMENT