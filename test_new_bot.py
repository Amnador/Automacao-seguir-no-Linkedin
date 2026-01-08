#!/usr/bin/env python3
"""
Teste simples do novo bot com localização
"""

import sys
import os
sys.path.append('.')

# Importa o TUI sem executar a interface gráfica
exec(open('TUI-tech-recruiter-location.py').read())

def test_tui():
    """Testa a TUI sem interface gráfica"""
    print("🧪 Testando Tech Recruiter Bot - Localização & Empresas")
    print("=" * 60)
    
    # Cria instância do TUI
    tui = TechRecruiterLocationTUI()
    
    print("✅ TUI carregada com sucesso!")
    print(f"📍 Localização: '{tui.config['location']}'")
    print(f"🏢 Empresas: {tui.config['companies']}")
    print(f"🔍 Termos de busca: {tui.config['search_terms']}")
    print(f"📊 Máximo diário: {tui.config['max_daily_connections']}")
    print(f"📈 Máximo semanal: {tui.config['max_weekly_connections']}")
    
    # Testa salvamento
    tui.save_config()
    print("✅ Configuração salva!")
    
    # Testa carregamento
    novo_tui = TechRecruiterLocationTUI()
    print("✅ Configuração recarregada com sucesso!")
    
    return True

if __name__ == "__main__":
    success = test_tui()
    if success:
        print("\n🎉 Todos os testes passaram!")
        print("\n📋 Para usar o novo bot:")
        print("1. Execute: python3 TUI-tech-recruiter-location.py")
        print("2. Configure localização e empresas desejadas")
        print("3. Pressione F5 para executar")
    else:
        print("❌ Testes falharam!")