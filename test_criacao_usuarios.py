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

def test_criacao_usuario(driver):
    # Acessar o site
    driver.get("https://www.giulianaflores.com.br")

    # Remover banners, cookies e popups
    driver.execute_script("""
        document.querySelectorAll('div[class*="DPOEasy"], div[role="dialog"]')
        .forEach(e => e.remove());
    """)

    # Clicar no link de perfil/login/cadastrar
    driver.execute_script("""
        document.querySelector("a[href*='login.aspx']").click();
    """)

    # Clicar em criar cadastro
    driver.execute_script("""
        document.querySelector("#ContentSite_ibtNewCustomer").click();
    """)

    # Preencher nome completo
    driver.find_element(By.ID, "ContentSite_txtName").send_keys("Andreia Melissa Barbosa")

    # Preencher CPF
    driver.find_element(By.ID, "ContentSite_txtCpf").send_keys("43287295519")

    # Preencher e-mail
    driver.find_element(By.ID, "ContentSite_txtEmail").send_keys("andreia.melissa.barbosa@muricy.com")

    # Remove possíveis overlays que bloqueiam o campo de senha
    driver.execute_script("""
        document.querySelectorAll('div[class*="DPOEasy"], div[role="dialog"]').forEach(e => e.remove());
    """)

    # Preencher senha 
    senha = None
    for _ in range(5):  
        try:
            senha = driver.find_element(By.ID, "ContentSite_txtPassword")
            if senha.is_displayed():
                senha.send_keys("AndMeBar.01")
                break
        except:
            driver.implicitly_wait(1)  

    # Preencher CEP
    cep = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'Zip')]"))
    )
    cep.clear()
    cep.send_keys("41218-034")

    # Clicar no OK do CEP 
    driver.execute_script("""
        const btn = document.querySelector("input[type='button'][id*='Zip'], button[id*='Zip']");
        if (btn) btn.click();
    """)

    # Preencher número do endereço
    numero = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'Number')]"))
    )
    numero.clear()
    numero.send_keys("351")

    # Preencher telefone
    driver.execute_script(
    "document.querySelector('input[name*=\"Phone\"]').value = '71992095363';"
    )

    # Clicar no botão finalizar cadastro 
    try:
        finalizar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "ContentSite_btnRegister"))
        )
        finalizar.click()
    except:
        print("Botão Finalizar cadastro não encontrado ou não clicável.")

    # Fecha pop-up final, se existir
    try:
        fechar_pop = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".fechar-pop-up, .close-modal"))
        )
        fechar_pop.click()
    except:
        pass

    