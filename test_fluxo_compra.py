import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def test_fluxo_compra(driver):
    driver.get("https://www.giulianaflores.com.br")
    wait = WebDriverWait(driver, 20)

    # Remove popups
    driver.execute_script(
        'document.querySelectorAll("div[class*=\'DPOEasy\'], div[role=\'dialog\']").forEach(e => e.remove());'
    )

    # Banner Oferta 24h
    banner = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "span.banner-titulo")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", banner)

    # Selecionar Produto
    produto = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "span.text4")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", produto)

    # Preencher o campo de CEP
    cep_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ContentSite_txtZip"))
    )
    cep_input.clear()  # Limpa caso tenha algo
    cep_input.send_keys("04935060")  # Insere o CEP

    # Clicar no botão OK
    ok_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.btn_okcep.jOpenShippingPopup"))
    )
    ok_button.click()

    # Remove popups
    driver.execute_script(
        'document.querySelectorAll("div[class*=\'DPOEasy\'], div[role=\'dialog\']").forEach(e => e.remove());'
    )

   # Clicar no segundo botão OK (confirmar dados de envio)
    confirm_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "btConfirmShippingData"))
    )
    confirm_button.click()

    # Clicar no X para fechar anuncio
    try:
        WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-close"))
        ).click()
    except:
        pass

    # Clicar no botao continuar
    driver.execute_script("""
    var el = document.getElementById('ContentSite_Basketcontrol1_rptBasket_imbFinalize_0');
    if (el) el.click();
    """)








