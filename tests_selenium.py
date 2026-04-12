from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()

try:

    # Test 1 — Registration
    driver.get("http://127.0.0.1:8000/register/")

    time.sleep(2)

    driver.find_element(By.NAME, "name").send_keys("Selenium User")

    driver.find_element(By.NAME, "email").send_keys("selenium2@gmail.com")

    driver.find_element(By.NAME, "password").send_keys("123456")

    driver.find_element(By.NAME, "confirm_password").send_keys("123456")

    driver.find_element(
        By.XPATH,
        "//button[@type='submit']"
    ).click()

    time.sleep(3)

    print("Registration Test Passed")


    # Test 2 — Login
    driver.get("http://127.0.0.1:8000/login/")

    time.sleep(2)

    driver.find_element(
        By.NAME,
        "email"
    ).send_keys("selenium2@gmail.com")

    driver.find_element(
        By.NAME,
        "password"
    ).send_keys("123456")

    driver.find_element(
        By.XPATH,
        "//button[@type='submit']"
    ).click()

    time.sleep(3)

    print("Login Test Passed")


    # Test 3 — University Search
    driver.get("http://127.0.0.1:8000/universities/")

    time.sleep(2)

    driver.find_element(
        By.NAME,
        "search"
    ).send_keys("MIT")

    time.sleep(3)

    print("Search Test Passed")


finally:

    driver.quit()