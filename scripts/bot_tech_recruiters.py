#!/usr/bin/env python3
import datetime
import os
import sys
import time
import platform
from random import *
from random import randint, random

import nodriver as uc
from nodriver import *

# Configurações do bot
TECH_RECRUITER_KEYWORDS = [
    "tech recruiter", "technical recruiter", "talent acquisition", 
    "recruitment specialist", "headhunter", "talent hunter",
    "recruiter", "hr specialist", "human resources"
]

DEFAULT_MESSAGE = """Olá! Sou desenvolvedor de software em busca de novas oportunidades na área de tecnologia. 
Estou aberto a vagas de desenvolvimento web, mobile e backend. 
Seria um prazer me conectar e explorar possíveis oportunidades."""

if len(sys.argv) > 4:
    browserPath = sys.argv[1]
    profilePath = sys.argv[2]
    LoggedIn = int(sys.argv[3])
    # Lê a mensagem de um arquivo se fornecido
    if len(sys.argv) > 5 and sys.argv[4] == "--message-file":
        try:
            with open(sys.argv[5], 'r', encoding='utf-8') as f:
                customMessage = f.read()
        except:
            customMessage = DEFAULT_MESSAGE
    else:
        customMessage = DEFAULT_MESSAGE
else:
    # Configurações padrão baseadas no sistema operacional
    system = platform.system()
    if system == "Darwin":  # MacOS
        browserPath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        profilePath = os.path.expanduser("~/Library/Application Support/Google/Chrome/Profile 1/")
    elif system == "Linux":
        browserPath = "/usr/bin/chromium"
        profilePath = "/home/capi/Documents/botdata/"
    else:  # Windows ou outros
        browserPath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        profilePath = "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data"
    LoggedIn = 1
    customMessage = DEFAULT_MESSAGE


def is_tech_recruiter(profile_text):
    """Verifica se o perfil é de um tech recruiter baseado nas palavras-chave"""
    if not profile_text:
        return False
    
    profile_text_lower = profile_text.lower()
    return any(keyword in profile_text_lower for keyword in TECH_RECRUITER_KEYWORDS)


async def send_connection_request(tab, connect_button, message):
    """Envia solicitação de conexão com mensagem personalizada"""
    try:
        # Clica no botão de conectar
        await connect_button.click()
        time.sleep(2 + 3 * random())
        
        # Procura pelo botão "Add a note" ou similar
        add_note_button = await tab.find("Add a note", timeout=10)
        if add_note_button:
            await add_note_button.click()
            time.sleep(1 + 2 * random())
            
            # Procura pelo campo de texto da mensagem
            message_field = await tab.find("custom-message", timeout=10)
            if message_field:
                await message_field.send_keys(message)
                time.sleep(1 + 2 * random())
                
                # Envia a solicitação
                send_button = await tab.find("Send invitation", timeout=10)
                if send_button:
                    await send_button.click()
                    return True
        
        # Se não conseguir adicionar mensagem, envia sem mensagem
        send_button = await tab.find("Send without note", timeout=5)
        if send_button:
            await send_button.click()
            return True
            
        return False
    except Exception as e:
        print(f"Erro ao enviar solicitação: {e}")
        return False


async def get_profile_info(tab, profile_element):
    """Obtém informações do perfil para verificar se é tech recruiter"""
    try:
        # Tenta encontrar o título/cargo da pessoa
        title_element = await profile_element.find("span[class*='entity-result__title-text']", timeout=5)
        if title_element:
            title_text = await title_element.get_text()
            return title_text
        return ""
    except:
        return ""


async def main():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    total_accounts = 0
    tech_recruiters_connected = 0
    Skip = 0

    if not os.path.exists("AccountLog.txt"):
        open("AccountLog.txt", "w").close()

    with open("AccountLog.txt", "r") as log_file:
        for line in log_file:
            if " on " not in line:
                continue
            parts = line.strip().split(" on ")
            if len(parts) < 2:
                continue
            accounts_part = parts[0]
            date_part = parts[1]

            try:
                accounts_count = int(accounts_part.split(": ")[1])
            except (IndexError, ValueError):
                continue

            try:
                log_date = datetime.datetime.strptime(date_part, "%Y-%m-%d")
            except ValueError:
                continue

            if log_date >= datetime.datetime.now() - datetime.timedelta(days=7):
                total_accounts += accounts_count

    if total_accounts >= 100:
        Skip = 1
        print("Total de contas esta semana: " + str(total_accounts))

    with open("AccountLog.txt", "r") as log_file:
        for line in log_file:
            if current_date in line:
                Skip = 1
                print(
                    "A data atual ("
                    + current_date
                    + ") já está no arquivo de log."
                )
                print("Total de contas esta semana: " + str(total_accounts))

    if not Skip:
        x = 0
        y = 0
        try:
            driver = await uc.start(
                headless=False,
                browser_executable_path=browserPath,
                user_data_dir=profilePath,
                browser_args=[
                    f"--window-size={randint(500, 1920)},{randint(500, 1080)}",
                ],
            )

            # Navega para a página de network com filtros de busca
            tab = await driver.get("https://www.linkedin.com/search/results/people/?keywords=tech%20recruiter&network=%5B%22S%22%5D")
            
            if LoggedIn:
                await driver.wait(time=random())  # Pausa aleatória
                
                # Aguarda os resultados da busca carregarem
                await tab.wait_for_element("div[class*='entity-result']", timeout=25)
                
                # Rola a página para carregar mais resultados
                while y < 5:  # Limita o número de scrolls
                    await tab.scroll_down(500)
                    time.sleep(2 + 3 * random())
                    y += 1

                # Encontra todos os cards de perfil
                profile_cards = await tab.find_all("div[class*='entity-result__item']", timeout=25)
                
                print(f"Encontrados {len(profile_cards)} perfis")
                
                for card in profile_cards:
                    if x >= 15:  # Limite de conexões por execução
                        break
                    
                    try:
                        # Obtém informações do perfil
                        profile_info = await get_profile_info(tab, card)
                        
                        # Verifica se é tech recruiter
                        if is_tech_recruiter(profile_info):
                            print(f"Tech Recruiter encontrado: {profile_info}")
                            
                            # Procura o botão de conectar neste card
                            connect_button = await card.find("button[aria-label*='Connect']", timeout=5)
                            if not connect_button:
                                connect_button = await card.find("button[aria-label*='Invite']", timeout=5)
                            
                            if connect_button:
                                await connect_button.scroll_into_view()
                                
                                # Envia solicitação com mensagem
                                if await send_connection_request(tab, connect_button, customMessage):
                                    tech_recruiters_connected += 1
                                    print(f"Conectado com Tech Recruiter #{tech_recruiters_connected}")
                                
                                time.sleep(3 + 5 * random())
                                x += 1
                        
                    except Exception as e:
                        print(f"Erro ao processar perfil: {e}")
                        continue

                with open("AccountLog.txt", "a") as log_file:
                    log_file.write(f"Tech Recruiters connected: {tech_recruiters_connected} on {current_date}\n")

                print(f"Total de Tech Recruiters conectados: {tech_recruiters_connected}")
                await tab.close()
            else:
                input("Pressione Enter para continuar...")
                await tab.close()
        except Exception as e:
            print(e)
            if tech_recruiters_connected > 0:
                with open("AccountLog.txt", "a") as log_file:
                    log_file.write(f"Tech Recruiters connected: {tech_recruiters_connected} on {current_date}\n")
            if 'tab' in locals():
                await tab.close()


if __name__ == "__main__":
    uc.loop().run_until_complete(main())