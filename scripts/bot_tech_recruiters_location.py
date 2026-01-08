#!/usr/bin/env python3
"""
LinkedIn Tech Recruiter Bot - Localização e Empresas
Automatiza conexões com Tech Recruiters considerando localização e empresas desejadas
"""

import os
import time
import random
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import platform

class TechRecruiterLocationBot:
    def __init__(self):
        self.setup_paths()
        self.setup_config()
        
    def setup_paths(self):
        """Configura caminhos baseados no sistema operacional"""
        system = platform.system()
        
        if system == "Darwin":  # MacOS
            self.chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            self.profile_path = os.path.expanduser("~/Library/Application Support/Google/Chrome/Profile 1/")
        elif system == "Linux":
            self.chrome_path = "/usr/bin/chromium"
            self.profile_path = "/home/capi/Documents/botdata/"
        else:  # Windows
            self.chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            self.profile_path = "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data"
            
        # Arquivos de log
        self.log_file = "AccountLog.txt"
        self.connections_file = "connections.json"
        
    def setup_config(self):
        """Carrega configurações de localização e empresas"""
        self.config_file = "config_location.json"
        self.config = self.load_config()
        
    def load_config(self):
        """Carrega configurações salvas"""
        default_config = {
            "location": "",
            "companies": [],
            "search_terms": ["tech recruiter", "recrutador", "talent acquisition"],
            "max_daily_connections": 15,
            "max_weekly_connections": 100
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge com config padrão
                    for key, value in default_config.items():
                        if key not in loaded_config:
                            loaded_config[key] = value
                    return loaded_config
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
            
        return default_config
    
    def save_config(self):
        """Salva configurações"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"✅ Config salvo: {self.config_file}")
        except Exception as e:
            print(f"Erro ao salvar config: {e}")
    
    def setup_driver(self):
        """Configura o driver do Chrome"""
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={self.profile_path}")
        chrome_options.add_argument("--profile-directory=Profile 1")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        
        return driver
    
    def is_tech_recruiter(self, profile_text):
        """Verifica se é Tech Recruiter baseado no texto do perfil"""
        if not profile_text:
            return False
            
        keywords = [
            "tech recruiter", "technical recruiter", "recruiter", 
            "talent acquisition", "talent sourcer", "headhunter",
            "recrutador", "recrutamento", "contratação", "rh"
        ]
        
        text_lower = profile_text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def is_from_desired_company(self, company_text):
        """Verifica se é de uma empresa desejada"""
        if not company_text or not self.config["companies"]:
            return True  # Se não houver empresas específicas, aceita qualquer uma
            
        company_lower = company_text.lower()
        for company in self.config["companies"]:
            if company.lower() in company_lower:
                return True
        return False
    
    def is_in_location(self, location_text):
        """Verifica se está na localização desejada"""
        if not location_text or not self.config["location"]:
            return True  # Se não houver localização específica, aceita qualquer uma
            
        location_lower = location_text.lower()
        config_location = self.config["location"].lower()
        return config_location in location_lower or location_lower in config_location
    
    def get_connection_stats(self):
        """Obtém estatísticas de conexões do dia/semana"""
        today = datetime.now().strftime("%Y-%m-%d")
        week = datetime.now().strftime("%Y-W%U")
        
        daily_count = 0
        weekly_count = 0
        
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    for line in f:
                        if today in line and "Conexão enviada" in line:
                            daily_count += 1
                        if week in line and "Conexão enviada" in line:
                            weekly_count += 1
        except Exception as e:
            print(f"Erro ao ler logs: {e}")
            
        return daily_count, weekly_count
    
    def log_connection(self, name, profile_url, company, location):
        """Registra conexão no log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Conexão enviada: {name} | {company} | {location} | {profile_url}\n"
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
            print(f"✅ Log: {name} - {company}")
        except Exception as e:
            print(f"Erro ao salvar log: {e}")
    
    def send_connection_request(self, driver, profile_url):
        """Envia solicitação de conexão (sem mensagem)"""
        try:
            driver.get(profile_url)
            time.sleep(3 + random.random() * 2)
            
            # Procura pelo botão "Conectar" ou "Connect"
            try:
                connect_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Conectar') or contains(@aria-label, 'Connect')]"))
                )
                
                # Scroll até o botão
                driver.execute_script("arguments[0].scrollIntoView(true);", connect_button)
                time.sleep(1 + random.random())
                
                # Clica no botão
                driver.execute_script("arguments[0].click();", connect_button)
                time.sleep(2 + random.random() * 2)
                
                # Procura pelo botão de enviar (sem nota)
                try:
                    send_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Enviar convite') or contains(@aria-label, 'Send invitation') or contains(@aria-label, 'Send now')]"))
                    )
                    send_button.click()
                    time.sleep(1 + random.random())
                    return True
                    
                except TimeoutException:
                    # Se não encontrar o botão de enviar, tenta fechar o modal
                    try:
                        close_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Dismiss') or contains(@aria-label, 'Fechar')]")
                        close_button.click()
                    except:
                        pass
                    return False
                    
            except TimeoutException:
                print("Botão Conectar não encontrado")
                return False
                
        except Exception as e:
            print(f"Erro ao enviar solicitação: {e}")
            return False
    
    def search_recruiters(self, driver):
        """Busca Tech Recruiters no LinkedIn"""
        daily_count, weekly_count = self.get_connection_stats()
        
        print(f"📊 Estatísticas atuais:")
        print(f"   Diárias: {daily_count}/{self.config['max_daily_connections']}")
        print(f"   Semanais: {weekly_count}/{self.config['max_weekly_connections']}")
        
        if daily_count >= self.config['max_daily_connections']:
            print("⚠️ Limite diário atingido!")
            return
            
        if weekly_count >= self.config['max_weekly_connections']:
            print("⚠️ Limite semanal atingido!")
            return
        
        # Monta a busca
        search_terms = " OR ".join([f'"{term}"' for term in self.config["search_terms"]])
        location_filter = f' AND "{self.config["location"]}"' if self.config["location"] else ""
        
        search_query = f"({search_terms}){location_filter}"
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query.replace(' ', '%20')}"
        
        print(f"🔍 Buscando: {search_query}")
        driver.get(search_url)
        time.sleep(5)
        
        connections_sent = 0
        page = 1
        
        while connections_sent < (self.config['max_daily_connections'] - daily_count):
            print(f"📄 Página {page}")
            
            # Pega todos os cards de pessoas
            people_cards = driver.find_elements(By.XPATH, "//div[@data-view-name='search-entity-result']")
            
            if not people_cards:
                print("Nenhum resultado encontrado")
                break
            
            for card in people_cards:
                try:
                    # Extrai informações do card
                    name_element = card.find_element(By.XPATH, ".//span[@aria-hidden='true'][contains(@class, 'entity-result__title-text')]//a")
                    name = name_element.text.strip()
                    profile_url = name_element.get_attribute('href')
                    
                    # Pega informações de cargo/empresa
                    try:
                        subtitle_element = card.find_element(By.XPATH, ".//div[contains(@class, 'entity-result__primary-subtitle')]")
                        subtitle = subtitle_element.text.strip()
                    except:
                        subtitle = ""
                    
                    # Pega localização
                    try:
                        location_element = card.find_element(By.XPATH, ".//div[contains(@class, 'entity-result__secondary-subtitle')]")
                        location = location_element.text.strip()
                    except:
                        location = ""
                    
                    # Verifica se é Tech Recruiter
                    if not self.is_tech_recruiter(name + " " + subtitle):
                        continue
                    
                    # Verifica localização
                    if not self.is_in_location(location):
                        continue
                    
                    # Verifica empresa desejada
                    if not self.is_from_desired_company(subtitle):
                        continue
                    
                    # Verifica se já não está conectado
                    try:
                        card.find_element(By.XPATH, ".//span[contains(text(), 'Conectado') or contains(text(), 'Connected')]")
                        continue  # Já está conectado
                    except:
                        pass
                    
                    print(f"🎯 Encontrado: {name} | {subtitle} | {location}")
                    
                    # Abre o perfil em nova aba
                    driver.execute_script("window.open(arguments[0], '_blank');", profile_url)
                    driver.switch_to.window(driver.window_handles[-1])
                    
                    # Envia conexão
                    if self.send_connection_request(driver, profile_url):
                        self.log_connection(name, profile_url, subtitle, location)
                        connections_sent += 1
                        print(f"✅ Conexão enviada para {name}")
                        
                        # Verifica limites
                        if connections_sent >= (self.config['max_daily_connections'] - daily_count):
                            break
                    
                    # Volta para a página de busca
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2 + random.random() * 3)
                    
                except Exception as e:
                    print(f"Erro ao processar card: {e}")
                    continue
            
            # Próxima página
            try:
                next_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Próxima') or contains(@aria-label, 'Next')]")
                if next_button.is_enabled():
                    next_button.click()
                    page += 1
                    time.sleep(5)
                else:
                    break
            except:
                break
        
        print(f"🎉 Conexões enviadas hoje: {connections_sent}")
    
    def run(self):
        """Executa o bot"""
        print("🚀 Iniciando Tech Recruiter Bot - Localização & Empresas")
        print("=" * 60)
        
        # Mostra configurações atuais
        print(f"📍 Localização: {self.config['location'] or 'Qualquer'}")
        print(f"🏢 Empresas: {', '.join(self.config['companies']) or 'Qualquer'}")
        print(f"🔍 Termos: {', '.join(self.config['search_terms'])}")
        
        driver = None
        try:
            driver = self.setup_driver()
            self.search_recruiters(driver)
            
        except KeyboardInterrupt:
            print("\n⏹️ Bot interrompido pelo usuário")
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if driver:
                driver.quit()
            print("✅ Bot finalizado")

def main():
    bot = TechRecruiterLocationBot()
    bot.run()

if __name__ == "__main__":
    main()