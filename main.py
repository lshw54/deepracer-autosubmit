import os
import time
import configparser
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

# load config file
config = configparser.ConfigParser()
config.read('config.ini')

# load config setting
ACCOUNT = config["AUTH"]['ACCOUNT']
PASSWORD = config['AUTH']['PASSWORD']
#binary_prefix = config['PREFIX']['BINARY']
cd_prefix = config['PREFIX']['CHROMEDRIVER']

# setup webdriver
options = webdriver.ChromeOptions()
#options.binary_location = os.path.abspath(binary_prefix)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(os.path.abspath(cd_prefix), options=options)

# open the website
driver.get("https://console.aws.amazon.com/?nc2=h_m_mc")
# show website title
print('Now in page -', driver.title)

time.sleep(1)
print("Now Login to the Web")
time.sleep(1)
driver.find_element_by_id("resolving_input").click()
driver.find_element_by_id("resolving_input").send_keys(ACCOUNT)
time.sleep(1)
driver.find_element_by_id("next_button").click()
time.sleep(1)
driver.find_element_by_id("password").click()
driver.find_element_by_id("password").send_keys(PASSWORD)
time.sleep(1)
driver.find_element_by_id("signin_button").click()

time.sleep(2)
usr = driver.find_element_by_id("nav-usernameMenu").text
print("Login Successful -", usr)

if driver.title == "AWS 管理控制台" or 'AWS Management Console':
    print("Going to DeepRacer")
    time.sleep(0.3)
    driver.find_element_by_id("search-box-input").click()
    driver.find_element_by_id("search-box-input").send_keys("AWS DeepRacer")
    time.sleep(0.5)
    driver.find_element_by_id("search-box-input-dropdown").click()
else:
    pass

if driver.title == "DeepRacer":
    print(driver.title)
    time.sleep(0.5)
    driver.get(
        "https://console.aws.amazon.com/deepracer/home?region=us-east-1#summitLeague/arn%3Aaws%3Adeepracer%3Aus-east-1%3A%3Aleaderboard%2Fsummit-season-2020-09-tt/submitModel"
    )
    time.sleep(3)
    print("Selcet Model")
    driver.find_element_by_id("awsui-select-0-textbox").click()
    time.sleep(0.5)
    driver.find_element_by_id("awsui-select-0-dropdown-option-0").click()
    time.sleep(0.5)
    driver.find_elements_by_class_name("awsui-form-actions")
    x = driver.find_elements_by_css_selector(
        "button.awsui-button.awsui-button-variant-primary.awsui-hover-child-icons"
    )[0]
    x.click()
    time.sleep(0.4)
    print("Finish")
