# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 21:41:18 2025

@author: pratik
"""

#! python3
# -*- coding: utf-8 -*-
"""Naukri Daily update - Profile Update Only"""

import logging
import os
import sys
import time
from datetime import datetime
from random import choice, randint
from string import ascii_uppercase, digits

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# ===== CONFIGURATION =====
username = "aniketmorankar@gmail.com"
password = "Ani@8080662121"
mob = "8080662121"
NAUKRI_LOGIN_URL = "https://www.naukri.com/nlogin/login"
headless = True  # set False to watch browser

logging.basicConfig(
    level=logging.INFO, filename="naukri.log", format="%(asctime)s    : %(message)s"
)
os.environ["WDM_LOCAL"] = "1"
os.environ["WDM_LOG_LEVEL"] = "0"

def log_msg(message):
    print(message)
    logging.info(message)

def catch(error):
    _, _, exc_tb = sys.exc_info()
    msg = f"{type(error)} : {error} at Line {exc_tb.tb_lineno}"
    print(msg)
    logging.error(msg)

def getObj(locatorType):
    return {
        "ID": By.ID,
        "NAME": By.NAME,
        "XPATH": By.XPATH,
        "TAG": By.TAG_NAME,
        "CLASS": By.CLASS_NAME,
        "CSS": By.CSS_SELECTOR,
        "LINKTEXT": By.LINK_TEXT,
    }[locatorType.upper()]

def is_element_present(driver, how, what):
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True

def WaitTillElementPresent(driver, elementTag, locator="ID", timeout=30):
    result = False
    driver.implicitly_wait(0)
    for _ in range(timeout):
        time.sleep(1)
        try:
            if is_element_present(driver, getObj(locator), elementTag):
                result = True
                break
        except Exception:
            pass
    driver.implicitly_wait(3)
    return result

def GetElement(driver, elementTag, locator="ID"):
    try:
        def _get_element(_tag, _locator):
            _by = getObj(_locator)
            if is_element_present(driver, _by, _tag):
                return WebDriverWait(driver, 15).until(
                    lambda d: driver.find_element(_by, _tag)
                )
        return _get_element(elementTag, locator.upper())
    except Exception as e:
        catch(e)
    return None

def tearDown(driver):
    try:
        driver.close()
        log_msg("Driver Closed Successfully")
    except Exception as e:
        catch(e)
    try:
        driver.quit()
        log_msg("Driver Quit Successfully")
    except Exception as e:
        catch(e)

def LoadNaukri(headless):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popups")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options, service=ChromeService())
    log_msg("Chrome Launched")
    driver.implicitly_wait(5)
    driver.get(NAUKRI_LOGIN_URL)
    return driver

def naukriLogin():
    status = False
    driver = None
    try:
        driver = LoadNaukri(headless)

        if is_element_present(driver, By.ID, "usernameField"):
            GetElement(driver, "usernameField", "ID").send_keys(username)
            GetElement(driver, "passwordField", "ID").send_keys(password)
            GetElement(driver, "//button[text()='Login']", "XPATH").click()
            time.sleep(5)

            # Skip popups
            if is_element_present(driver, By.XPATH, "//*[contains(@class, 'cross-icon')]"):
                GetElement(driver, "//*[contains(@class, 'cross-icon')]", "XPATH").click()
            if is_element_present(driver, By.XPATH, "//*[text()='SKIP AND CONTINUE']"):
                GetElement(driver, "//*[text()='SKIP AND CONTINUE']", "XPATH").click()

        if WaitTillElementPresent(driver, "ff-inventory", "ID", 40):
            log_msg("Naukri Login Successful")
            status = True

    except Exception as e:
        catch(e)
    return (status, driver)

def UpdateProfile(driver):
    try:
        mobXpath = "//*[@name='mobile'] | //*[@id='mob_number']"
        saveXpath = "//button[@ type='submit'][@value='Save Changes'] | //*[@id='saveBasicDetailsBtn']"
        view_profile_locator = "//*[contains(@class, 'view-profile')]//a"
        edit_locator = "(//*[contains(@class, 'icon edit')])[1]"
        save_confirm = "//*[text()='today' or text()='Today']"
        close_locator = "//*[contains(@class, 'crossIcon')]"

        WaitTillElementPresent(driver, view_profile_locator, "XPATH", 20)
        GetElement(driver, view_profile_locator, "XPATH").click()
        time.sleep(2)

        if WaitTillElementPresent(driver, close_locator, "XPATH", 10):
            GetElement(driver, close_locator, "XPATH").click()
            time.sleep(2)

        if is_element_present(driver, By.XPATH, edit_locator):
            GetElement(driver, edit_locator, "XPATH").click()
            WaitTillElementPresent(driver, mobXpath, "XPATH", 10)
            mobField = GetElement(driver, mobXpath, "XPATH")
            if mobField:
                mobField.clear()
                mobField.send_keys(mob)
                time.sleep(1)
            GetElement(driver, saveXpath, "XPATH").send_keys(Keys.ENTER)
            time.sleep(3)

            if is_element_present(driver, By.XPATH, save_confirm):
                log_msg("Profile Update Successful")
            else:
                log_msg("Profile Update Failed")
    except Exception as e:
        catch(e)

def main():
    log_msg("----- Naukri Automation Started -----")
    driver = None
    try:
        status, driver = naukriLogin()
        if status:
            UpdateProfile(driver)
    except Exception as e:
        catch(e)
    finally:
        tearDown(driver)
    log_msg("----- Naukri Automation Ended -----\\n")

if __name__ == "__main__":
    main()
