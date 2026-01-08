#!/usr/bin/env python3
"""
Script de demonstração do Tech Recruiter Bot
Este script mostra como o bot funciona sem precisar executar o navegador
"""

import sys
import os

# Adiciona o diretório scripts ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Palavras-chave para identificar Tech Recruiters
TECH_RECRUITER_KEYWORDS = [
    "tech recruiter", "technical recruiter", "talent acquisition", 
    "recruitment specialist", "headhunter", "talent hunter",
    "recruiter", "hr specialist", "human resources"
]

def is_tech_recruiter(profile_text):
    """Verifica se o perfil é de um tech recruiter baseado nas palavras-chave"""
    if not profile_text:
        return False
    
    profile_text_lower = profile_text.lower()
    return any(keyword in profile_text_lower for keyword in TECH_RECRUITER_KEYWORDS)

def test_tech_recruiter_filter():
    """Testa o filtro de Tech Recruiters"""
    
    # Exemplos de títulos de perfis
    perfis_teste = [
        "Senior Software Engineer at Google",
        "Tech Recruiter | Talent Acquisition Specialist",
        "HR Manager - Human Resources",
        "Technical Recruiter at Meta",
        "Full Stack Developer",
        "Headhunter & Talent Hunter",
        "Recruitment Specialist - Tech",
        "Product Manager",
        "Talent Acquisition Partner",
        "DevOps Engineer"
    ]
    
    print("🔍 Testando filtro de Tech Recruiters")
    print("=" * 50)
    
    tech_recruiters_encontrados = []
    
    for perfil in perfis_teste:
        if is_tech_recruiter(perfil):
            tech_recruiters_encontrados.append(perfil)
            print(f"✅ TECH RECRUITER: {perfil}")
        else:
            print(f"❌ Não é Tech Recruiter: {perfil}")
    
    print("\n" + "=" * 50)
    print(f"📊 Total de Tech Recruiters encontrados: {len(tech_recruiters_encontrados)}")
    print(f"📋 Perfis filtrados: {tech_recruiters_encontrados}")
    
    return tech_recruiters_encontrados

def exemplo_mensagem():
    """Mostra um exemplo de mensagem de conexão"""
    
    mensagem_padrao = """Olá! Sou desenvolvedor de software em busca de novas oportunidades na área de tecnologia. 
Estou aberto a vagas de desenvolvimento web, mobile e backend. 
Seria um prazer me conectar e explorar possíveis oportunidades."""
    
    print("\n💬 Exemplo de mensagem de conexão:")
    print("=" * 50)
    print(mensagem_padrao)
    print("=" * 50)
    
    return mensagem_padrao

def main():
    print("🤖 Tech Recruiter Bot - Demonstração")
    print("=" * 50)
    
    # Testa o filtro
    recruiters = test_tech_recruiter_filter()
    
    # Mostra exemplo de mensagem
    mensagem = exemplo_mensagem()
    
    print(f"\n🎯 O bot irá:")
    print(f"   • Buscar apenas Tech Recruiters no LinkedIn")
    print(f"   • Enviar solicitações de conexão com mensagem personalizada")
    print(f"   • Limitar a 15 conexões por execução")
    print(f"   • Respeitar o limite semanal de 100 conexões")
    
    print(f"\n✨ Para executar o bot real:")
    print(f"   python3 TUI-tech-recruiter.py")
    
    # Salva estatísticas
    with open("demo_stats.txt", "w", encoding="utf-8") as f:
        f.write(f"Tech Recruiter Bot - Demonstração\n")
        f.write(f"Data: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Tech Recruiters encontrados no teste: {len(recruiters)}\n")
        f.write(f"Mensagem de conexão:\n{mensagem}\n")
    
    print(f"\n📄 Estatísticas salvas em: demo_stats.txt")

if __name__ == "__main__":
    import datetime
    main()