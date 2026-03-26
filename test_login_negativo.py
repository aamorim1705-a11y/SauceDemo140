import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

def test_login_negativo(driver):
    # Acessar o site
    driver.get("https://www.giulianaflores.com.br")

    # Remover banners, cookies e popups
    driver.execute_script("""
        document.querySelectorAll('div[class*="DPOEasy"], div[role="dialog"]')
        .forEach(e => e.remove());
    """)

    # Clicar no link de perfil/login
    driver.execute_script("""
        document.querySelector("a[href*='login.aspx']").click();
    """)

    # Preencher e-mail valido
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "ContentSite_txtEmail"))
    )
    email_input.send_keys("andreia.melissa.barbosa@muricy.com")

    # Preencher senha invalida
    senha_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "ContentSite_txtPassword"))
    )
    senha_input.send_keys("AndMeBar01")

    # Remover overlays 
    driver.execute_script("""
        document.querySelectorAll(
            'div[class*="DPOEasy"], div[role="dialog"], iframe, .modal, .overlay'
        ).forEach(e => e.remove());
    """)

    # Clicar no botão Continuar 
    driver.find_element(By.ID, "ContentSite_ibtLoginQuickEmail").click()

    

    