#!/usr/bin/env python3
"""
Teste do novo bot com localização - Versão simples
"""

import json
import os

class SimpleConfigTest:
    def __init__(self):
        self.config_file = "config_location.json"
        self.config = self.load_config()
    
    def load_config(self):
        """Carrega configurações salvas"""
        default_config = {
            "location": "São Paulo, Brasil",
            "companies": ["Google", "Amazon", "Microsoft", "Meta", "Apple"],
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
    
    def test_config(self):
        """Testa configurações"""
        print("🧪 Testando configurações do novo bot")
        print("=" * 50)
        
        print(f"📍 Localização: '{self.config['location']}'")
        print(f"🏢 Empresas: {self.config['companies']}")
        print(f"🔍 Termos: {self.config['search_terms']}")
        print(f"📊 Máx. diárias: {self.config['max_daily_connections']}")
        print(f"📈 Máx. semanais: {self.config['max_weekly_connections']}")
        
        # Testa busca com localização
        location_filter = f' AND "{self.config["location"]}"' if self.config["location"] else ""
        search_terms = " OR ".join([f'"{term}"' for term in self.config["search_terms"]])
        search_query = f"({search_terms}){location_filter}"
        
        print(f"\n🔍 Query de busca: {search_query}")
        
        # Testa URL de busca
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query.replace(' ', '%20')}"
        print(f"🔗 URL: {search_url}")
        
        return True

def test_bot_logic():
    """Testa lógica do bot"""
    print("\n🧪 Testando lógica do bot")
    print("=" * 50)
    
    # Testa detecção de Tech Recruiter
    def is_tech_recruiter(profile_text):
        keywords = [
            "tech recruiter", "technical recruiter", "recruiter", 
            "talent acquisition", "talent sourcer", "headhunter",
            "recrutador", "recrutamento", "contratação", "rh"
        ]
        text_lower = profile_text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    # Testa verificação de empresa
    companies = ["Google", "Amazon", "Microsoft"]
    def is_from_desired_company(company_text):
        if not company_text or not companies:
            return True
        company_lower = company_text.lower()
        for company in companies:
            if company.lower() in company_lower:
                return True
        return False
    
    # Testa verificação de localização
    location = "São Paulo"
    def is_in_location(location_text):
        if not location_text or not location:
            return True
        location_lower = location_text.lower()
        config_location = location.lower()
        return config_location in location_lower or location_lower in config_location
    
    # Testes
    test_profiles = [
        ("João Silva", "Tech Recruiter at Google", "São Paulo, Brasil", True),
        ("Maria Santos", "Senior Developer at Amazon", "São Paulo", False),  # Não é recruiter
        ("Pedro Oliveira", "Talent Acquisition Specialist at Microsoft", "Remote", True),
        ("Ana Costa", "HR Manager at Meta", "Rio de Janeiro", True),  # É RH mas fora da localização
    ]
    
    print("Testando perfis:")
    for name, title, loc, expected in test_profiles:
        is_recruiter = is_tech_recruiter(title)
        is_company = is_from_desired_company(title)
        is_loc = is_in_location(loc)
        
        result = is_recruiter and is_company and is_loc
        status = "✅" if result == expected else "❌"
        
        print(f"{status} {name}: {title} | {loc}")
        print(f"   Recruiter: {is_recruiter} | Empresa: {is_company} | Local: {is_loc}")
        print()

def main():
    print("🚀 Testando Tech Recruiter Bot - Localização & Empresas")
    print("=" * 60)
    
    # Testa configurações
    tester = SimpleConfigTest()
    tester.test_config()
    
    # Testa lógica
    test_bot_logic()
    
    # Salva config
    tester.save_config()
    
    print("\n🎉 Testes concluídos!")
    print("\n📋 Próximos passos:")
    print("1. Execute: python3 TUI-tech-recruiter-location.py")
    print("2. Configure sua localização e empresas desejadas")
    print("3. Pressione F5 para executar o bot")
    print("\n💡 Dicas:")
    print("• Use 'Remote' para vagas remotas")
    print("• Separe empresas por vírgula: Google, Amazon, Microsoft")
    print("• Use cidades como 'São Paulo', 'Rio de Janeiro', 'Brasil'")

if __name__ == "__main__":
    main()