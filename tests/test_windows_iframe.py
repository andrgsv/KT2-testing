from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)


def test_windows():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://the-internet.herokuapp.com/windows")

        main_window = driver.current_window_handle

        link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
        )
        link.click()

        wait.until(EC.number_of_windows_to_be(2))

        for window in driver.window_handles:
            if window != main_window:
                driver.switch_to.window(window)
                break

        wait.until(lambda d: "New Window" in d.page_source)

        assert "New Window" in driver.page_source

        driver.close()
        driver.switch_to.window(main_window)

    finally:
        driver.quit()


def test_iframe():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://the-internet.herokuapp.com/iframe")

        iframe = wait.until(
            EC.presence_of_element_located((By.ID, "mce_0_ifr"))
        )

        driver.switch_to.frame(iframe)

        body = wait.until(
            EC.presence_of_element_located((By.ID, "tinymce"))
        )

        driver.execute_script(
            "arguments[0].innerText = 'Selenium iframe test';",
            body
        )

        assert "Selenium iframe test" in body.text

        driver.switch_to.default_content()

    finally:
        driver.quit()