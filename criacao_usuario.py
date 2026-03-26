import pytest
from selenium import webdriver
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--incognito")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.notifications": 2
    })
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_criacao_usuario(driver):
    driver.get("https://www.giulianaflores.com.br")

    driver.execute_script("""
        document.querySelectorAll('div[class*="DPOEasy"], div[role="dialog"]')
        .forEach(e => e.remove());
    """)

    driver.execute_script("""
        document.querySelector("a[href*='login.aspx']").click();
    """)

    driver.execute_script("""
        document.querySelector("#ContentSite_ibtNewCustomer").click();
    """)

    driver.find_element(By.ID, "ContentSite_txtName").send_keys(
        "Raquel Lívia Porto"
    )

    driver.find_element(By.ID, "ContentSite_txtCpf").send_keys(
        "82282571550"
    )

    driver.find_element(By.ID, "ContentSite_txtEmail").send_keys(
        "raquel.livia.porto@valeguinchos.com.br"
    )

    driver.find_element(By.ID, "ContentSite_txtPassword").send_keys(
        "PZhj2aH5YL"
    )

    driver.find_element(By.ID, "ContentSite_txtConfirmPassword").send_keys(
        "PZhj2aH5YL"
    )
   
