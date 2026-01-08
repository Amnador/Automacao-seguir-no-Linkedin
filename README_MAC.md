# 🍎 LinkedIn Tech Recruiter Bot - Guia para MacOS

## 📋 Visão Geral
Este bot foi adaptado especificamente para MacOS e permite que você se conecte apenas com Tech Recruiters no LinkedIn, enviando uma mensagem personalizada de apresentação.

## ✅ Requisitos do Sistema
- **Sistema Operacional**: macOS 10.15 (Catalina) ou superior
- **Python**: 3.7 ou superior
- **Google Chrome**: Versão mais recente
- **Processador**: Intel ou Apple Silicon (M1/M2)

## 🚀 Instalação Rápida

### Opção 1: Script Automático
```bash
# Tornar o script executável e executar
chmod +x install_mac.sh
./install_mac.sh
```

### Opção 2: Instalação Manual
```bash
# 1. Instalar Python 3 (se necessário)
brew install python3

# 2. Instalar dependências
pip3 install selenium webdriver-manager

# 3. Instalar Google Chrome (se necessário)
brew install --cask google-chrome
```

## 🎯 Como Usar

### 1. Executar o Bot
```bash
# Na pasta do projeto
python3 TUI-tech-recruiter.py
```

### 2. Configurar no TUI
- **Selecione**: "Tech Recruiter Mode (Linux)"
- **Caminho do Chrome**: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- **Perfil**: `~/Library/Application Support/Google/Chrome/Profile 1/`
- **Mensagem**: Personalize sua mensagem de conexão

### 3. Fazer Login no LinkedIn
Quando o Chrome abrir:
1. Faça login no LinkedIn
2. Aguarde o bot iniciar automaticamente
3. O bot buscará Tech Recruiters e enviará solicitações

## 📁 Caminhos Importantes no MacOS

| Finalidade | Caminho |
|------------|---------|
| Chrome App | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` |
| Perfil Chrome | `~/Library/Application Support/Google/Chrome/Profile 1/` |
| Logs do Bot | `~/Documents/trae_projects/bot connect/LinkedIn-Bot-Followers/AccountLog.txt` |
| Python 3 | `/usr/bin/python3` |

## 🔧 Arquivos do Projeto

- **[bot_tech_recruiters_selenium.py](scripts/bot_tech_recruiters_selenium.py)** - Bot principal (versão Selenium)
- **[TUI-tech-recruiter.py](TUI-tech-recruiter.py)** - Interface de configuração
- **[demo_tech_recruiter.py](demo_tech_recruiter.py)** - Teste do filtro
- **[test_mac_compatibility.py](test_mac_compatibility.py)** - Teste de compatibilidade

## 🛡️ Segurança e Limites

- **Limite Diário**: 15 conexões por execução
- **Limite Semanal**: 100 conexões totais
- **Delay entre ações**: 2-8 segundos (aleatório)
- **Detecção de perfis**: Apenas Tech Recruiters via palavras-chave

## 🚨 Solução de Problemas

### Chrome não abre
```bash
# Verificar se Chrome está instalado
ls -la "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Reinstalar Chrome
brew reinstall --cask google-chrome
```

### Erro de permissão
```bash
# Dar permissão de execução
chmod +x scripts/*.py
chmod +x *.py
```

### Python não encontra módulos
```bash
# Reinstalar dependências
pip3 install --force-reinstall selenium webdriver-manager
```

### ChromeDriver não encontrado
O bot usa `webdriver-manager` que baixa automaticamente o ChromeDriver correto.

## 💡 Dicas para MacOS

1. **Segurança**: Você pode precisar permitir o Chrome em "Preferências > Segurança e Privacidade"
2. **Atalho**: Adicione um alias no `.zshrc`:
   ```bash
   alias linkedin-bot='cd ~/Documents/trae_projects/bot\ connect/LinkedIn-Bot-Followers && python3 TUI-tech-recruiter.py'
   ```
3. **Terminal**: Use o Terminal ou iTerm2 para melhor experiência
4. **Logs**: Monitore o progresso em `AccountLog.txt`

## ⚠️ Avisos Importantes

- **LinkedIn**: Use com moderação para evitar restrições na conta
- **Mensagens**: Mantenha mensagens profissionais e curtas
- **Frequência**: Não execute mais de 1 vez por dia
- **Backup**: Faça backup do seu perfil Chrome antes de usar

## 🎯 Exemplo de Mensagem de Conexão
```
Olá! Sou desenvolvedor de software em busca de novas oportunidades na área de tecnologia. 
Estou aberto a vagas de desenvolvimento web, mobile e backend. 
Seria um prazer me conectar e explorar possíveis oportunidades.
```

## 📞 Suporte

Se encontrar problemas:
1. Execute `python3 test_mac_compatibility.py` para verificar
2. Verifique os logs em `AccountLog.txt`
3. Certifique-se de que está usando os caminhos corretos do MacOS

---
**Desenvolvido para MacOS com ❤️**