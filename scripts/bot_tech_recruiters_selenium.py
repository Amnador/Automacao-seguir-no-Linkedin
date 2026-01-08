#!/usr/bin/env python3
"""
Bot para LinkedIn - Tech Recruiter Edition (usando Selenium)
Versão compatível com MacOS e mais estável
"""

import datetime
import os
import sys
import time
import platform
from random import randint, random, uniform

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium não instalado. Instale com: pip3 install selenium")

# Palavras-chave para identificar Tech Recruiters
TECH_RECRUITER_KEYWORDS = [
    "tech recruiter", "technical recruiter", "talent acquisition", 
    "recruitment specialist", "headhunter", "talent hunter",
    "recruiter", "hr specialist", "human resources", "staffing"
]

# Mensagem padrão
DEFAULT_MESSAGE = """Olá! Sou desenvolvedor de software em busca de novas oportunidades na área de tecnologia. 
Estou aberto a vagas de desenvolvimento web, mobile e backend. 
Seria um prazer me conectar e explorar possíveis oportunidades."""

def get_system_paths():
    """Retorna os caminhos padrão baseados no sistema operacional"""
    system = platform.system()
    if system == "Darwin":  # MacOS
        return {
            "browser": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "profile": os.path.expanduser("~/Library/Application Support/Google/Chrome/Profile 1/"),
            "driver": None  # Usará o ChromeDriver automático
        }
    elif system == "Linux":
        return {
            "browser": "/usr/bin/chromium",
            "profile": "/home/capi/Documents/botdata/",
            "driver": "/usr/bin/chromedriver"
        }
    else:  # Windows
        return {
            "browser": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "profile": "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data",
            "driver": "chromedriver.exe"
        }

def is_tech_recruiter(profile_text):
    """Verifica se o perfil é de um tech recruiter baseado nas palavras-chave"""
    if not profile_text:
        return False
    
    profile_text_lower = profile_text.lower()
    return any(keyword in profile_text_lower for keyword in TECH_RECRUITER_KEYWORDS)

def setup_driver(browser_path, profile_path, headless=False):
    """Configura e retorna o driver do Chrome"""
    chrome_options = Options()
    
    # Configurações básicas
    chrome_options.add_argument(f"--user-data-dir={profile_path}")
    chrome_options.add_argument("--profile-directory=Profile 1")
    chrome_options.add_argument(f"--window-size={randint(1024, 1920)},{randint(768, 1080)}")
    
    if headless:
        chrome_options.add_argument("--headless")
    
    # Configurações adicionais para evitar detecção
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Tenta usar o ChromeDriver automático (mais fácil para Mac)
        if platform.system() == "Darwin":
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            # Para Linux/Windows, usa caminho específico
            driver = webdriver.Chrome(options=chrome_options)
        
        return driver
    except Exception as e:
        print(f"❌ Erro ao criar driver: {e}")
        return None

def send_connection_request(driver, profile_url, message):
    """Envia solicitação de conexão com mensagem personalizada"""
    try:
        driver.get(profile_url)
        time.sleep(3 + random() * 2)
        
        # Procura pelo botão "Conectar" ou "Connect"
        try:
            connect_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Conectar') or contains(@aria-label, 'Connect')]"))
            )
            
            # Scroll até o botão
            driver.execute_script("arguments[0].scrollIntoView(true);", connect_button)
            time.sleep(1 + random())
            
            # Clica no botão
            driver.execute_script("arguments[0].click();", connect_button)
            time.sleep(2 + random() * 2)
            
            # Procura por "Adicionar nota" ou "Add a note"
            try:
                add_note = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Adicionar nota') or contains(text(), 'Add a note')]"))
                )
                add_note.click()
                time.sleep(1 + random())
                
                # Escreve a mensagem
                message_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "custom-message"))
                )
                message_field.clear()
                message_field.send_keys(message)
                time.sleep(1 + random())
                
                # Envia o convite
                send_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Enviar convite') or contains(@aria-label, 'Send invitation') or contains(@aria-label, 'Send now')]"))
                )
                send_button.click()
                
                return True
                
            except TimeoutException:
                # Se não conseguir adicionar nota, envia sem mensagem
                try:
                    send_without_note = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Enviar sem nota') or contains(text(), 'Send without note')]"))
                    )
                    send_without_note.click()
                    return True
                except TimeoutException:
                    return False
                    
        except TimeoutException:
            print("Botão Conectar não encontrado")
            return False
            
    except Exception as e:
        print(f"Erro ao enviar solicitação: {e}")
        return False

def search_tech_recruiters(driver, max_pages=3):
    """Busca Tech Recruiters no LinkedIn"""
    base_url = "https://www.linkedin.com/search/results/people/?keywords=tech%20recruiter&network=%5B%22S%22%5D"
    recruiters_found = []
    
    for page in range(1, max_pages + 1):
        url = f"{base_url}&page={page}"
        driver.get(url)
        time.sleep(3 + random() * 2)
        
        try:
            # Aguarda os resultados carregarem
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "entity-result__item"))
            )
            
            # Encontra todos os cards de perfil
            profile_cards = driver.find_elements(By.CLASS_NAME, "entity-result__item")
            
            for card in profile_cards:
                try:
                    # Obtém informações do perfil
                    title_element = card.find_element(By.CLASS_NAME, "entity-result__title-text")
                    title_text = title_element.text
                    
                    # Verifica se é Tech Recruiter
                    if is_tech_recruiter(title_text):
                        # Obtém o link do perfil
                        link_element = card.find_element(By.TAG_NAME, "a")
                        profile_url = link_element.get_attribute("href")
                        
                        recruiters_found.append({
                            'title': title_text,
                            'url': profile_url
                        })
                        
                        print(f"✅ Tech Recruiter encontrado: {title_text}")
                    
                except NoSuchElementException:
                    continue
                    
        except TimeoutException:
            print(f"⏰ Timeout na página {page}")
            continue
    
    return recruiters_found

def main():
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium não está disponível. Por favor, instale:")
        print("   pip3 install selenium webdriver-manager")
        return
    
    # Configurações
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    total_accounts = 0
    tech_recruiters_connected = 0
    skip = False
    
    # Verifica arquivo de log
    if not os.path.exists("AccountLog.txt"):
        open("AccountLog.txt", "w").close()
    
    # Verifica limites semanais e diários
    with open("AccountLog.txt", "r") as log_file:
        for line in log_file:
            if " on " not in line:
                continue
            parts = line.strip().split(" on ")
            if len(parts) < 2:
                continue
            
            try:
                accounts_count = int(parts[0].split(": ")[1])
                log_date = datetime.datetime.strptime(parts[1], "%Y-%m-%d")
                
                # Verifica limite semanal
                if log_date >= datetime.datetime.now() - datetime.timedelta(days=7):
                    total_accounts += accounts_count
                
                # Verifica se já executou hoje
                if current_date in line:
                    skip = True
                    
            except (ValueError, IndexError):
                continue
    
    if total_accounts >= 100:
        print("❌ Limite semanal atingido!")
        return
    
    if skip:
        print(f"❌ Bot já executou hoje ({current_date})!")
        return
    
    # Obtém caminhos do sistema
    paths = get_system_paths()
    
    # Configura o driver
    print("🚀 Iniciando Chrome...")
    driver = setup_driver(paths["browser"], paths["profile"])
    
    if not driver:
        print("❌ Falha ao iniciar o Chrome!")
        return
    
    try:
        # Faz login no LinkedIn (se necessário)
        driver.get("https://www.linkedin.com/login")
        time.sleep(5)
        
        # Verifica se está na página de login
        if "login" in driver.current_url:
            print("⚠️  Por favor, faça login manualmente no LinkedIn")
            input("Pressione Enter após fazer login...")
        
        # Busca Tech Recruiters
        print("🔍 Buscando Tech Recruiters...")
        recruiters = search_tech_recruiters(driver, max_pages=2)
        
        print(f"📊 Encontrados {len(recruiters)} Tech Recruiters")
        
        # Envia solicitações de conexão
        for recruiter in recruiters[:15]:  # Limite de 15 por execução
            if tech_recruiters_connected >= 15:
                break
                
            print(f"📤 Conectando com: {recruiter['title']}")
            
            if send_connection_request(driver, recruiter['url'], DEFAULT_MESSAGE):
                tech_recruiters_connected += 1
                print(f"✅ Conexão enviada #{tech_recruiters_connected}")
            else:
                print(f"❌ Falha ao conectar")
            
            # Espera entre conexões
            time.sleep(5 + random() * 5)
        
        # Registra no log
        with open("AccountLog.txt", "a") as log_file:
            log_file.write(f"Tech Recruiters connected: {tech_recruiters_connected} on {current_date}\n")
        
        print(f"🎉 Total de Tech Recruiters conectados: {tech_recruiters_connected}")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        
    finally:
        driver.quit()
        print("🏁 Bot finalizado")

if __name__ == "__main__":
    main()