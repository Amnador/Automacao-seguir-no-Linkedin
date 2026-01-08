#!/usr/bin/env python3
"""
TUI - Tech Recruiter Bot com Localização e Empresas
Interface para configurar e executar o bot com filtros de localização
"""

import curses
import os
import subprocess
import json
import platform

def get_system_paths():
    """Retorna os caminhos padrão baseados no sistema operacional"""
    system = platform.system()
    if system == "Darwin":  # MacOS
        return {
            "browser": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "profile": os.path.expanduser("~/Library/Application Support/Google/Chrome/Profile 1/"),
            "python": "/usr/bin/python3"
        }
    elif system == "Linux":
        return {
            "browser": "/usr/bin/chromium",
            "profile": "/home/capi/Documents/botdata/",
            "python": "/usr/bin/python3"
        }
    else:  # Windows
        return {
            "browser": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "profile": "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data",
            "python": "python"
        }

class TechRecruiterLocationTUI:
    def __init__(self):
        self.config_file = "config_location.json"
        self.config = self.load_config()
        self.current_field = 0
        self.fields = [
            "location",
            "companies", 
            "search_terms",
            "max_daily_connections",
            "max_weekly_connections"
        ]
        
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
            pass
            
        return default_config
    
    def save_config(self):
        """Salva configurações"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            pass
    
    def draw_header(self, stdscr):
        """Desenha o cabeçalho"""
        try:
            height, width = stdscr.getmaxyx()
            
            # Verifica se o terminal é grande o suficiente
            if height < 10 or width < 60:
                stdscr.clear()
                stdscr.addstr(0, 0, "ERRO: Terminal muito pequeno!")
                stdscr.addstr(1, 0, "Por favor, aumente a janela do terminal.")
                stdscr.addstr(2, 0, "Mínimo: 60x10 caracteres")
                stdscr.refresh()
                stdscr.getch()
                return False
            
            title = "Tech Recruiter Bot - Localizacao & Empresas"
            subtitle = "Configure filtros para encontrar Tech Recruiters"
            
            # Remove emojis para evitar problemas de codificação
            if curses.has_colors():
                stdscr.attron(curses.A_BOLD)
            
            # Centraliza o título apenas se couber
            title_x = max(0, (width - len(title)) // 2)
            if title_x + len(title) < width:
                stdscr.addstr(1, title_x, title)
            
            if curses.has_colors():
                stdscr.attroff(curses.A_BOLD)
            
            # Subtítulo
            subtitle_x = max(0, (width - len(subtitle)) // 2)
            if subtitle_x + len(subtitle) < width and 2 < height:
                stdscr.addstr(2, subtitle_x, subtitle)
            
            # Linha divisória
            if 3 < height:
                stdscr.addstr(3, 0, "=" * min(width, 80))
            
            return True
        except curses.error:
            return False
    
    def draw_field(self, stdscr, y, label, value, is_selected):
        """Desenha um campo de formulário"""
        try:
            if y >= stdscr.getmaxyx()[0] - 1:  # Verifica se cabe na tela
                return
                
            if is_selected:
                stdscr.attron(curses.A_REVERSE)
            
            # Label do campo
            if y < stdscr.getmaxyx()[0] and 4 < stdscr.getmaxyx()[1]:
                stdscr.addstr(y, 4, f"{label}:")
            
            if is_selected:
                stdscr.attroff(curses.A_REVERSE)
                stdscr.attron(curses.A_BOLD)
            
            # Mostra valor do campo
            if isinstance(value, list):
                value_str = ", ".join(value)
            else:
                value_str = str(value)
                
            # Limita o valor para caber na tela
            max_width = stdscr.getmaxyx()[1] - 25
            if max_width > 0 and y < stdscr.getmaxyx()[0]:
                stdscr.addstr(y, 25, value_str[:max_width])
            
            if is_selected:
                stdscr.attroff(curses.A_BOLD)
        except curses.error:
            pass
    
    def draw_help(self, stdscr):
        """Desenha ajuda na parte inferior"""
        try:
            height, width = stdscr.getmaxyx()
            
            help_text = [
                "Navegacao: | Editar: ENTER | Salvar: F2 | Executar: F5 | Sair: ESC",
                "Dicas:",
                "• Localizacao: Cidade, Estado ou Pais (ex: 'Sao Paulo', 'Remote')",
                "• Empresas: Separe por virgula (ex: Google, Amazon, Microsoft)",
                "• Termos: Palavras-chave para encontrar Tech Recruiters"
            ]
            
            # Remove emojis e caracteres especiais para evitar problemas
            y = max(0, height - len(help_text) - 2)
            for text in help_text:
                if y < height - 1 and len(text) < width - 4:
                    stdscr.addstr(y, 2, text)
                y += 1
        except curses.error:
            pass
    
    def edit_field(self, stdscr, field_name, current_value):
        """Edita um campo"""
        height, width = stdscr.getmaxyx()
        
        # Limpa a linha de edição
        edit_win = curses.newwin(3, width - 6, height // 2 - 1, 3)
        edit_win.box()
        
        if field_name == "companies":
            prompt = "Empresas (separe por vírgula): "
            current_str = ", ".join(current_value)
        elif field_name == "search_terms":
            prompt = "Termos de busca (separe por vírgula): "
            current_str = ", ".join(current_value)
        else:
            prompt = f"{field_name.replace('_', ' ').title()}: "
            current_str = str(current_value)
        
        edit_win.addstr(1, 2, prompt)
        curses.echo()
        curses.curs_set(1)
        
        try:
            new_value = edit_win.getstr(1, len(prompt) + 2, 50).decode('utf-8')
            
            if field_name in ["companies", "search_terms"]:
                # Converte para lista
                new_list = [item.strip() for item in new_value.split(',') if item.strip()]
                if new_list:
                    self.config[field_name] = new_list
            elif field_name in ["max_daily", "max_weekly"]:
                # Converte para número
                try:
                    self.config[field_name] = int(new_value)
                except ValueError:
                    pass
            else:
                self.config[field_name] = new_value
                
        except:
            pass
        finally:
            curses.noecho()
            curses.curs_set(0)
            edit_win.clear()
    
    def execute_bot(self):
        """Executa o bot"""
        self.save_config()
        
        # Caminho do script
        script_path = os.path.join("scripts", "bot_tech_recruiters_location.py")
        
        if not os.path.exists(script_path):
            return False, "Script não encontrado"
        
        try:
            # Executa o bot
            result = subprocess.run(
                [get_system_paths()["python"], script_path],
                capture_output=True,
                text=True,
                cwd="."
            )
            
            if result.returncode == 0:
                return True, "Bot executado com sucesso!"
            else:
                return False, f"Erro: {result.stderr}"
                
        except Exception as e:
            return False, f"Erro ao executar: {e}"
    
    def main_screen(self, stdscr):
        """Tela principal"""
        try:
            curses.curs_set(0)
            stdscr.clear()
            
            while True:
                stdscr.clear()
                height, width = stdscr.getmaxyx()
                
                # Verifica tamanho mínimo do terminal
                if height < 15 or width < 60:
                    stdscr.clear()
                    stdscr.addstr(0, 0, "ERRO: Terminal muito pequeno!")
                    stdscr.addstr(1, 0, f"Tamanho atual: {width}x{height}")
                    stdscr.addstr(2, 0, "Mínimo necessário: 60x15")
                    stdscr.addstr(3, 0, "Aumente a janela e pressione R para recarregar...")
                    stdscr.refresh()
                    
                    key = stdscr.getch()
                    if key == ord('r') or key == ord('R'):
                        continue
                    elif key == 27:  # ESC
                        break
                    continue
                
                # Desenha cabeçalho
                if not self.draw_header(stdscr):
                    continue
                
                # Campos
                y = 6
                fields_data = [
                    ("Localizacao", self.config["location"]),
                    ("Empresas Desejadas", self.config["companies"]),
                    ("Termos de Busca", self.config["search_terms"]),
                    ("Max. Diarias", self.config["max_daily_connections"]),
                    ("Max. Semanais", self.config["max_weekly_connections"])
                ]
                
                for i, (label, value) in enumerate(fields_data):
                    if y < height - 5:  # Deixa espaço para ajuda
                        self.draw_field(stdscr, y, label, value, i == self.current_field)
                    y += 2
                
                self.draw_help(stdscr)
                stdscr.refresh()
                
                # Navegação
                key = stdscr.getch()
                
                if key == curses.KEY_UP:
                    self.current_field = max(0, self.current_field - 1)
                elif key == curses.KEY_DOWN:
                    self.current_field = min(len(fields_data) - 1, self.current_field + 1)
                elif key == ord('\n') or key == curses.KEY_ENTER:
                    # Edita o campo atual
                    field_name = self.fields[self.current_field]
                    self.edit_field(stdscr, field_name, self.config[field_name])
                elif key == curses.KEY_F2:
                    # Salva configuração
                    self.save_config()
                    if height > 10:
                        stdscr.addstr(height - 1, 2, "Configuracao salva! Pressione qualquer tecla...")
                        stdscr.getch()
                elif key == curses.KEY_F5:
                    # Executa bot
                    if height > 10:
                        stdscr.addstr(height - 1, 2, "Executando bot...")
                        stdscr.refresh()
                    
                    success, message = self.execute_bot()
                    
                    # Mostra resultado
                    try:
                        result_win = curses.newwin(5, 60, max(0, height // 2 - 2), max(0, width // 2 - 30))
                        result_win.box()
                        result_win.addstr(2, 2, message[:50])
                        result_win.addstr(3, 2, "Pressione qualquer tecla para continuar...")
                        result_win.getch()
                    except curses.error:
                        # Se não conseguir criar janela, mostra mensagem simples
                        stdscr.clear()
                        stdscr.addstr(0, 0, message)
                        stdscr.addstr(1, 0, "Pressione qualquer tecla para continuar...")
                        stdscr.getch()
                        
                elif key == 27:  # ESC
                    break
        except curses.error as e:
            # Erro crítico do curses
            stdscr.clear()
            stdscr.addstr(0, 0, f"Erro na interface: {str(e)}")
            stdscr.addstr(1, 0, "Pressione qualquer tecla para sair...")
            stdscr.getch()
    
    def run(self):
        """Executa a interface TUI"""
        curses.wrapper(self.main_screen)

if __name__ == "__main__":
    tui = TechRecruiterLocationTUI()
    tui.run()