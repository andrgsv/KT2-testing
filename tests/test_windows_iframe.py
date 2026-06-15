
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_windows():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/windows")

    main = driver.current_window_handle

    driver.find_element(By.LINK_TEXT, "Click Here").click()
    time.sleep(2)

    for h in driver.window_handles:
        if h != main:
            driver.switch_to.window(h)

    assert "New Window" in driver.title

    driver.close()
    driver.switch_to.window(main)
    driver.quit()


def test_iframe():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/iframe")

    driver.switch_to.frame("mce_0_ifr")

    body = driver.find_element(By.ID, "tinymce")
    body.clear()
    body.send_keys("Hello from Selenium KT2 test")

    driver.switch_to.default_content()

    assert "iframe" in driver.current_url

    driver.quit()
