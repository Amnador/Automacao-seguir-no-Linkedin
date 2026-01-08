#!/bin/bash
# Script de instalação para MacOS - Tech Recruiter Bot com Localização

echo "🚀 Instalando Tech Recruiter Bot - Localização & Empresas"
echo "============================================================"

# Verifica se é MacOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Este script é específico para MacOS"
    exit 1
fi

# Atualiza pip
echo "📦 Atualizando pip..."
python3 -m pip install --upgrade pip

# Instala dependências
echo "📦 Instalando dependências..."
pip3 install selenium webdriver-manager

# Torna scripts executáveis
echo "🔧 Tornando scripts executáveis..."
chmod +x scripts/bot_tech_recruiters_location.py
chmod +x TUI-tech-recruiter-location.py

# Cria diretório de logs se não existir
mkdir -p logs

# Cria configuração inicial
echo "📝 Criando configuração inicial..."
cat > config_location.json << EOF
{
  "location": "São Paulo, Brasil",
  "companies": ["Google", "Amazon", "Microsoft", "Meta", "Apple"],
  "search_terms": ["tech recruiter", "recrutador", "talent acquisition"],
  "max_daily_connections": 15,
  "max_weekly_connections": 100
}
EOF

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Execute: python3 TUI-tech-recruiter-location.py"
echo "2. Configure sua localização e empresas desejadas"
echo "3. Pressione F5 para executar o bot"
echo ""
echo "💡 Dicas de uso:"
echo "• Use 'Remote' para vagas remotas"
echo "• Separe empresas por vírgula: Google, Amazon, Microsoft"
echo "• Use cidades como 'São Paulo', 'Rio de Janeiro', 'Brasil'"
echo "• O bot conecta apenas com Tech Recruiters (sem mensagens)"
echo ""
echo "📁 Arquivos criados:"
echo "• config_location.json - Suas configurações"
echo "• AccountLog.txt - Log de conexões"
echo "• connections.json - Histórico de conexões"
echo ""
echo "🎯 Boa caçada de Tech Recruiters!"