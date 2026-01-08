# 🎯 Bot Conexão Tech - LinkedIn

> *"Conectando talentos com oportunidades, uma mensagem de cada vez"*

Um bot inteligente que identifica e se conecta com Tech Recruiters no LinkedIn, facilitando sua jornada de networking profissional.

## 🌟 Sobre Este Projeto

Este bot foi desenvolvido com um propósito simples mas poderoso: **ajudar profissionais de tecnologia a se conectarem com os melhores recrutadores do mercado**. Em vez de seguir aleatoriamente, nosso bot identifica perfis de Tech Recruiters e envia mensagens personalizadas demonstrando seu interesse em oportunidades.

### � A Filosofia por Trás

Acreditamos que networking não é sobre quantidade, mas sobre **qualidade de conexões**. Cada conexão deve ser significativa e trazer valor para ambos os lados. Por isso, nosso bot:

- 🎯 **Foca em Tech Recruiters especificamente**
- 💬 **Envia mensagens personalizadas e autênticas**
- 🔒 **Respeita os limites do LinkedIn** (15 conexões/dia, 100/semana)
- 🧠 **Usa inteligência para identificar os melhores perfis**

## 🚀 Funcionalidades

### Modo Tech Recruiter
- **Identificação Inteligente**: Detecta perfis de Tech Recruiters usando palavras-chave específicas
- **Mensagens Personalizadas**: Envia mensagens autênticas sobre sua busca por oportunidades
- **Filtros por Localização**: Conecte-se com recrutadores de sua região ou empresas desejadas
- **Interface TUI Amigável**: Configure tudo facilmente através de uma interface no terminal

### Características de Segurança
- ✅ **Limites Diários**: Máximo de 15 conexões por dia
- ✅ **Limites Semanais**: Máximo de 100 conexões por semana
- ✅ **Detecção de Execução**: Evita execuções múltiplas no mesmo dia
- ✅ **Logs Detalhados**: Acompanhe todas as ações realizadas

## 🎨 Interface TUI

Nossa interface em terminal é colorida e intuitiva:

```
🎯 Tech Recruiter Bot - Localização & Empresas
Configure filtros para encontrar os melhores Tech Recruiters

Localização: São Paulo, Brasil
Empresas Desejadas: Google, Amazon, Microsoft, Meta, Apple
Termos de Busca: tech recruiter, recrutador, talent acquisition
Máx. Diárias: 15
Máx. Semanais: 100

Navegação: ↑↓ | Editar: ENTER | Salvar: F2 | Executar: F5 | Sair: ESC
```

## 🛠️ Instalação para MacOS

### Método 1: Script Automático (Recomendado)
```bash
# Torne o script executável
chmod +x install_mac.sh

# Execute a instalação
./install_mac.sh
```

### Método 2: Instalação Manual
```bash
# Instale o Python 3.6+ (se ainda não tiver)
brew install python

# Instale as dependências
pip3 install selenium webdriver-manager

# Instale o Google Chrome (se ainda não tiver)
brew install --cask google-chrome
```

## 📋 Como Usar

### 1. Configure seu Ambiente
```bash
# Navegue até o diretório
cd LinkedIn-Bot-Followers

# Execute a interface TUI
python3 TUI-tech-recruiter-location.py
```

### 2. Configure seus Filtros
- **Localização**: "São Paulo", "Remote", "Brasil", etc.
- **Empresas Desejadas**: "Google, Amazon, Microsoft, Meta, Apple"
- **Termos de Busca**: Já vem pré-configurado com termos de Tech Recruiters

### 3. Execute o Bot
- Pressione **F5** para iniciar
- Faça login no LinkedIn quando o Chrome abrir
- O bot começará a identificar e conectar com Tech Recruiters

## 🎯 Exemplos de Mensagens

O bot envia mensagens como:
> "Olá! Sou [seu nome], profissional de tecnologia com experiência em [sua área]. Estou explorando novas oportunidades e gostaria de me conectar para ficar por dentro de vagas interessantes na empresa. Obrigado!"

## 🔧 Scripts Disponíveis

- **`TUI-tech-recruiter-location.py`**: Interface principal com filtros de localização
- **`TUI-tech-recruiter.py`**: Interface básica para Tech Recruiters
- **`scripts/bot_tech_recruiters_selenium.py`**: Bot principal (MacOS/Linux)
- **`install_mac.sh`**: Script de instalação para MacOS

## 🌟 Diferenciais

### Por que este bot é especial?
- **Focado em Qualidade**: Não é sobre quantidade de conexões, mas sobre conexões certas
- **Respeitoso**: Segue todos os limites do LinkedIn para manter sua conta segura
- **Inteligente**: Identifica recrutadores reais, não perfis aleatórios
- **Personalizável**: Adapte mensagens e filtros ao seu estilo

### Para Quem é Este Bot?
- 👨‍💻 **Desenvolvedores** buscando novas oportunidades
- �‍💼 **Profissionais de Tech** querendo expandir seu network
- 🎯 **Recém-formados** entrando no mercado de tecnologia
- 🚀 **Profissionais em transição** de carreira

## ⚠️ Importante

Este bot foi criado com **responsabilidade e ética** em mente. Use-o de forma consciente:

- ✅ **Seja autêntico** nas suas mensagens
- ✅ **Respeite os limites** do LinkedIn
- ✅ **Use com moderação** - qualidade sobre quantidade
- ❌ **Não spame** recrutadores
- ❌ **Não automessage** em excesso

## 🤝 Contribuindo

Adoramos contribuições! Se você tem ideias para melhorar o bot:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📧 Suporte

Encontrou um bug ou tem uma sugestão? Abra uma [issue](https://github.com/Capi-nemoo/LinkedIn-Bot-Followers/issues) ou entre em contato!

---

> *"O sucesso não é sobre quem você conhece, mas sobre quem conhece você pelo trabalho que você faz."*

**Feito com ❤️ para a comunidade tech**