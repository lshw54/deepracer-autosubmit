import os
import re
import time
from core.logger import Logger
from core.config import Config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = Logger(logger="Auto-Submit").getlog()
config = Config()
# setup webdriver
options = webdriver.ChromeOptions()
#options.binary_location = config.binary_prefix
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(config.cd_prefix, options=options)
# open the website
driver.get("https://console.aws.amazon.com")
driver.implicitly_wait(10)
logger.info(driver.title)


def login():
    if config.login_type.lower() == 'root':
        logger.info(u'Using the % s user Sign-in' % config.login_type.upper())
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'resolving_input'))).send_keys(config.account)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'next_button'))).click()
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'password'))).send_keys(config.password)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'signin_button'))).click()
            time.sleep(5)
            if driver.find_element_by_id('error_title').text == 'Authentication failed':
                logger.warning(
                    u'Your authentication information is incorrect. Please try again.')
                exit()
        except NoSuchElementException:
            usr = driver.find_element_by_id("nav-usernameMenu").text
            logger.info(u"Login Successful - %s" % usr)
    elif config.login_type.lower() == 'iam':
        logger.info(u'Using the % s user Sign-in' % config.login_type.upper())
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'iam_user_radio_button'))).click()
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'resolving_input'))).send_keys(config.accountid)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'next_button'))).click()
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'username'))).send_keys(config.account)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'password'))).send_keys(config.password)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'signin_button'))).click()
            time.sleep(5)
            if driver.find_element_by_class_name('mainError.ng-binding.ng-scope').text == 'Your authentication information is incorrect. Please try again.':
                logger.warning(
                    u'Your authentication information is incorrect. Please try again.')
        except NoSuchElementException:
            usr = driver.find_element_by_id("nav-usernameMenu").text
            logger.info(u"Login Successful - %s" % usr)
            # try:
            #    element = WebDriverWait(driver, 10).until(
            #        EC.presence_of_element_located((By.ID, "myDynamicElement")))


def submit():
    # Go to the submit page
    if driver.title == "AWS 管理控制台" or 'AWS Management Console':
        logger.info(u'Going to DeepRacer Page')
        driver.get('https://console.aws.amazon.com/deepracer/')
        driver.find_elements_by_partial_link_text(
            'AWS Summit Online')[0].click()
        logger.info(u'AWS Summit Online')
        driver.find_elements_by_xpath(
            "//*[@aria-labelledby='awsui-cards-2-0-header']")
        driver.find_elements_by_css_selector(
            'button.awsui-button.awsui-button-variant-normal.awsui-hover-child-icons')[0].click()
        vn = driver.find_elements_by_id(
            'PLCHLDR_leaderboard_summary_view_name')[0].text
        logger.info(vn)
        time.sleep(10)
        while True:
            x = driver.find_elements_by_css_selector(
                "button.awsui-button.awsui-button-variant-primary.awsui-hover-child-icons")[0]
            time.sleep(10)
            if x == x:
                time.sleep(10)
                x.click()
                time.sleep(10)
                driver.find_element_by_class_name(
                    "awsui-select-trigger-icon").click()
                time.sleep(10)
                # driver.find_element_by_id("awsui-select-0-dropdown-option-0").click()
                driver.find_elements_by_xpath(
                    "//*[@title='" + config.md_name + "']")[0].click()
                time.sleep(10)
                driver.find_elements_by_class_name("awsui-form-actions")
                a = driver.find_elements_by_css_selector(
                    "button.awsui-button.awsui-button-variant-primary.awsui-hover-child-icons")[0]
                a.click()
                time.sleep(600)
                logger.info(u'Rank - %s' %
                            driver.find_elements_by_id('PLCHLDR_league_rank')[0].text)
                logger.info(u'Latest model submitted - %s' %
                            driver.find_elements_by_id('PLCHLDR_latest_model_name')[0].text)
                logger.info(
                    u'Time - %s' % driver.find_elements_by_id('PLCHLDR_latest_model_time')[0].text)
                logger.info(u'Submission time - %s' %
                            driver.find_elements_by_id('PLCHLDR_latest_model_submission_time')[0].text)


def main():
    login()
    submit()


if __name__ == "__main__":
    main()
