# 1 - Bibliotecas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 2 - Classe (Opcional)
class Teste_Produtos():

    # 2.1 Atributos
    url = "https://www.saucedemo.com"              # endereço do site alvo

    # 2.2 Funções e Métodos
    def setup_method(self, method):
        options = Options()
        options.add_argument("--incognito")                   
        self.driver = webdriver.Chrome(options=options)     # instancia o objeto do Selenium WebDriver como Chrome
        self.driver.implicitly_wait(10)                     # define o tempo de espera padrão por elementos em 10 segundos

    def teardown_method(self, method):             # método de finalização dos testes
        self.driver.quit()                         # encerra / destrói o objeto do Selenium WebDriver da memória

    def test_selecionar_produto(self):             # método de teste
        self.driver.get(self.url)                  # abre o navegador
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")               # escreve no campo user-name
        self.driver.find_element(By.NAME, "password").send_keys("secret_sauce")               # escreve a senha
        self.driver.find_element(By.CSS_SELECTOR, "input.submit-button.btn_action").click()   # clique no botão de login

        # Valida pagina de produtos
        assert self.driver.find_element(By.CLASS_NAME, "title").text == "Products"                # confirma se está escrito Products no elemento
        assert self.driver.find_element(By.ID, "item_4_title_link").text == "Sauce Labs Backpack" # confirma se é a mochila
        
        # Confirma o preço da mochila
        assert self.driver.find_element(By.CSS_SELECTOR, ".inventory_item:nth-child(1) .inventory_item_price").text == (
            "$29.99" 
        )

        # Adiciona o produto ao carrinho
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()           # clique no botao de adicionar produto ao carrinho
        
        # Clica no carrinho e valida o produto
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").click()                               # clique no botao do carrinho
        assert self.driver.find_element(By.CLASS_NAME, "inventory_item_name").text == "Sauce Labs Backpack"  # valida o produto no carrinho
       
        # Confirma se o preço e a quantidade do produto adicionado está correto
        assert self.driver.find_element(By.CLASS_NAME, "inventory_item_price").text == "$29.99"
        assert self.driver.find_element(By.CSS_SELECTOR, ".cart_quantity").text == "1"

        # Remove o produto e faz logout
        self.driver.find_element(By.ID, "remove-sauce-labs-backpack").click()    # clica no botao remover item do carrinho
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()         # clica no menu burger
        self.driver.find_element(By.ID, "logout_sidebar_link").click()           # clica no logout
  