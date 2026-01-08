#!/bin/bash
# Script de instalação para MacOS - LinkedIn Tech Recruiter Bot

echo "🚀 Instalador LinkedIn Tech Recruiter Bot - MacOS"
echo "=================================================="

# Verifica se é MacOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Este script é apenas para MacOS!"
    exit 1
fi

# Atualiza pip
echo "📦 Atualizando pip..."
python3 -m pip install --upgrade pip

# Instala dependências
echo "📦 Instalando dependências..."
pip3 install selenium webdriver-manager

# Verifica Google Chrome
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -f "$CHROME_PATH" ]; then
    echo "⚠️  Google Chrome não encontrado!"
    echo "📥 Por favor, instale o Google Chrome:"
    echo "   brew install --cask google-chrome"
    echo "   ou baixe em: https://www.google.com/chrome/"
    read -p "Pressione Enter após instalar o Chrome..."
fi

# Cria diretório de perfil se não existir
PROFILE_DIR="$HOME/Library/Application Support/Google/Chrome/Profile 1"
if [ ! -d "$PROFILE_DIR" ]; then
    echo "📁 Criando diretório de perfil..."
    mkdir -p "$PROFILE_DIR"
fi

# Torna os scripts executáveis
chmod +x scripts/*.py
chmod +x *.py

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Execute: python3 TUI-tech-recruiter.py"
echo "2. Selecione 'Tech Recruiter Mode (Linux)'"
echo "3. Configure sua mensagem de conexão"
echo "4. Faça login no LinkedIn quando o Chrome abrir"
echo ""
echo "💡 Dicas:"
echo "- O bot buscará apenas Tech Recruiters"
echo "- Enviará sua mensagem personalizada"
echo "- Limite: 15 conexões por dia, 100 por semana"
echo ""
echo "🔧 Arquivos importantes:"
echo "- scripts/bot_tech_recruiters_selenium.py (bot principal)"
echo "- TUI-tech-recruiter.py (interface de configuração)"
echo "- demo_tech_recruiter.py (teste do filtro)"