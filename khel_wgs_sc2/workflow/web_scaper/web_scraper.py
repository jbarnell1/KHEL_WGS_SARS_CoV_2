
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("https://wgs.app.clearlabs.com/login")
    driver.find_element_by_id("cl-field-login-email").send_keys("jonathan.barnell@ks.gov")
    driver.find_element_by_id("cl-field-password-email").send_keys("")