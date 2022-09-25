import os
import time
import urllib
import argparse

from core.config import Config
from core.logger import Logger
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

logger = Logger(logger="Auto-Submit").getlog()
config = Config()

def open_browser(args):
    '''
    Windows User need to set the binary and chromedrive path
    '''
    options = Options()
    #options.binary_location = config.binary_prefix
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")
    #options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #browser = webdriver.Chrome(config.cd_prefix, options=options)
    browser = webdriver.Chrome(ChromeDriverManager().install())
    return browser

def colse_browser(args, browser):
    try:
        browser.close()
    except Exception:
        logger.debug("Error", Exception)

def login(args, browser):
    logger.info("Using {} account to login.".format(config.account))

    url = "https://{}.signin.aws.amazon.com/console".format(config.accountid)
    browser.get(url)
    logger.info(browser.title)
    time.sleep(5)

    browser.find_element_by_id("username").send_keys(config.account)
    browser.find_element_by_id("password").send_keys(config.password)
    browser.find_element_by_id("signin_button").click()
    time.sleep(5)

    usr = browser.find_element_by_id("nav-usernameMenu").text
    logger.info("Login Successful - {}".format(usr))

    time.sleep(5)


def submit_model(args, browser):
    logger.info("Try to submit the {} model".format(config.md_name))

    url = "{}/{}{}/submitModel".format(config.league_url, urllib.parse.quote_plus(config.arn), config.league_name)
    
    while True:
        try:
            browser.get(url)
            # time.sleep(10)
            # try:
            #     browser.find_element(By.XPATH, "//body").click()
            #     browser.find_element(By.XPATH, '//div[@id="PLCHLDR__new_car_reward_modal"]').click()
            # except Exception:
            #     logger.debug("Error", Exception)
            #     #browser.save_screenshot(screenshot)
            #     #post_slack(doc, "{} : {}".format(args.target, ex), screenshot)
            
            time.sleep(10)

            browser.find_element(By.CSS_SELECTOR, "button[class^='awsui_button-trigger']").click()

            path = '//*[@title="{}"]'.format(config.md_name)
            browser.find_element_by_xpath(path).click()
            browser.find_element(By.CSS_SELECTOR, "button[class*='awsui_variant-primary']").click()

            time.sleep(10)
            logger.info("Success submit the {} model".format(config.md_name))
            time.sleep(600)
            logger.info(u'Rank - %s' %
                        browser.find_elements_by_id('PLCHLDR_league_rank')[0].text)
            logger.info(u'Latest model submitted - %s' %
                        browser.find_elements_by_id('PLCHLDR_latest_model_name')[0].text)
            logger.info(
                u'Time - %s' % browser.find_elements_by_id('PLCHLDR_latest_model_time')[0].text)
            logger.info(u'Submission time - %s' %
                            browser.find_elements_by_id('PLCHLDR_latest_model_submission_time')[0].text)

        except Exception:
            logger.debug("Error", Exception)

def main():
    args = argparse.ArgumentParser()
    browser = open_browser(args)
    login(args, browser)
    submit_model(args, browser)
    colse_browser(args, browser)


if __name__ == "__main__":
    main()