#!/usr/bin/env python3
"""
Teste de compatibilidade para MacOS - LinkedIn Tech Recruiter Bot
Verifica se os caminhos e dependências estão corretos
"""

import os
import platform
import subprocess

def test_mac_compatibility():
    """Testa a compatibilidade com MacOS"""
    
    print("🧪 Teste de Compatibilidade - MacOS")
    print("=" * 50)
    
    # Verifica o sistema operacional
    system = platform.system()
    print(f"✅ Sistema Operacional: {system}")
    
    if system != "Darwin":
        print("⚠️  Este teste é específico para MacOS!")
        return False
    
    # Verifica versão do macOS
    version = platform.mac_ver()[0]
    print(f"✅ Versão do macOS: {version}")
    
    # Testa caminho do Chrome
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(chrome_path):
        print(f"✅ Google Chrome encontrado: {chrome_path}")
    else:
        print(f"❌ Google Chrome não encontrado: {chrome_path}")
        print("📥 Instale com: brew install --cask google-chrome")
        return False
    
    # Testa diretório de perfil
    profile_path = os.path.expanduser("~/Library/Application Support/Google/Chrome/Profile 1/")
    if os.path.exists(os.path.dirname(profile_path)):
        print(f"✅ Diretório de perfil Chrome: {profile_path}")
    else:
        print(f"⚠️  Diretório de perfil não existe, será criado: {profile_path}")
    
    # Testa Python 3
    try:
        result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
        print(f"✅ Python 3: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Python 3 não encontrado!")
        return False
    
    # Testa Selenium
    try:
        import selenium
        print("✅ Biblioteca Selenium: Instalada")
    except ImportError:
        print("❌ Biblioteca Selenium: Não instalada")
        print("📥 Instale com: pip3 install selenium webdriver-manager")
        return False
    
    # Testa leitura do bot Selenium
    try:
        with open("scripts/bot_tech_recruiters_selenium.py", "r") as f:
            content = f.read()
            if "Darwin" in content and "platform.system()" in content:
                print("✅ Bot adaptado para MacOS: Sim")
            else:
                print("⚠️  Bot adaptado para MacOS: Parcial")
    except FileNotFoundError:
        print("❌ Bot não encontrado")
        return False
    except FileNotFoundError:
        print("❌ Arquivo bot_tech_recruiters.py não encontrado!")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Teste concluído! O bot está pronto para uso no Mac.")
    print("\n📋 Próximos passos:")
    print("1. Execute: python3 TUI-tech-recruiter.py")
    print("2. Selecione 'Tech Recruiter Mode (Linux)'")
    print("3. Configure sua mensagem de conexão")
    print("4. O bot buscará Tech Recruiters no LinkedIn!")
    
    return True

def show_mac_paths():
    """Mostra os caminhos padrão do Mac"""
    print("\n📁 Caminhos Padrão no Mac:")
    print("-" * 30)
    print(f"Chrome: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    print(f"Perfil: {os.path.expanduser('~/Library/Application Support/Google/Chrome/Profile 1/')}")
    print(f"Python: {subprocess.run(['which', 'python3'], capture_output=True, text=True).stdout.strip()}")
    print(f"Diretório atual: {os.getcwd()}")

if __name__ == "__main__":
    success = test_mac_compatibility()
    show_mac_paths()
    
    if success:
        print("\n✨ Tudo certo! Seu Mac está pronto para executar o Tech Recruiter Bot.")
    else:
        print("\n🔧 Por favor, corrija os problemas acima antes de executar o bot.")