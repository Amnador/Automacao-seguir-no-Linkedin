import curses
import os
import subprocess
import platform


def mainOS(stdscr):
    curses.curs_set(0)
    options = ["Windows", "Linux", "Tech Recruiter Mode (Linux)"]
    current_index = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select your OS (q to exit):")
        for i, option in enumerate(options):
            if i == current_index:
                stdscr.addstr(i + 2, 0, option, curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, option)
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and current_index > 0:
            current_index -= 1
        elif key == curses.KEY_DOWN and current_index < len(options) - 1:
            current_index += 1
        elif key in [10, 13]:
            break
        elif key == ord("q"):
            return None
    return current_index


def get_input(stdscr, prompt, default_value=""):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    if default_value:
        stdscr.addstr(1, 0, default_value)
    stdscr.refresh()
    input_str = stdscr.getstr(2, 0).decode("utf-8")
    if not input_str.strip() and default_value:
        input_str = default_value
    curses.noecho()
    return input_str


def get_multiline_input(stdscr, prompt, default_message=""):
    """Obtém entrada de texto multilinha para a mensagem de conexão"""
    lines = []
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.addstr(1, 0, "Pressione Enter para nova linha, Ctrl+D para finalizar:")
    
    if default_message:
        stdscr.addstr(3, 0, "Mensagem padrão (pressione Enter para usar ou escreva uma nova):")
        stdscr.addstr(4, 0, default_message[:80] + "..." if len(default_message) > 80 else default_message)
    
    stdscr.refresh()
    
    # Coleta linhas até o usuário pressionar Ctrl+D (EOF)
    while True:
        try:
            stdscr.addstr(6 + len(lines), 0, f"Linha {len(lines) + 1}: ")
            stdscr.refresh()
            line = stdscr.getstr(6 + len(lines), 10).decode("utf-8")
            if line:
                lines.append(line)
            else:
                break
        except:
            break
    
    return "\n".join(lines) if lines else default_message


def get_default_paths():
    """Retorna os caminhos padrão baseados no sistema operacional"""
    system = platform.system()
    if system == "Darwin":  # MacOS
        return {
            "browser": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "profile": os.path.expanduser("~/Library/Application Support/Google/Chrome/Profile 1/")
        }
    elif system == "Linux":
        return {
            "browser": "/usr/bin/chromium",
            "profile": "/home/capi/Documents/botdata/"
        }
    else:  # Windows
        return {
            "browser": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "profile": "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data"
        }


def main(stdscr):
    os_choice = mainOS(stdscr)
    if os_choice is None:
        return
    
    default_paths = get_default_paths()
    
    browser_path = get_input(stdscr, "Enter the Chrome executable path:", default_paths["browser"])
    profile_path = get_input(stdscr, "Enter the profile path:", default_paths["profile"])
    logged_in = get_input(stdscr, "Are you logged in? (1 for yes, 0 for no):", "1")
    
    # Configurações específicas para o modo Tech Recruiter
    if os_choice == 2:  # Tech Recruiter Mode
        message = get_multiline_input(stdscr, "Enter your connection message for Tech Recruiters:",
                                    "Olá! Sou desenvolvedor de software em busca de novas oportunidades na área de tecnologia. Estou aberto a vagas de desenvolvimento web, mobile e backend. Seria um prazer me conectar e explorar possíveis oportunidades.")
        
        # Salva a mensagem em um arquivo temporário
        message_file = "temp_message.txt"
        with open(message_file, 'w', encoding='utf-8') as f:
            f.write(message)
        
        file_to_run = os.path.join("./scripts", "bot_tech_recruiters.py")
        stdscr.clear()
        stdscr.addstr(0, 0, f"Running Tech Recruiter bot...")
        stdscr.refresh()
        subprocess.run(["python", file_to_run, browser_path, profile_path, logged_in, "--message-file", message_file])
        
        # Limpa o arquivo temporário
        if os.path.exists(message_file):
            os.remove(message_file)
            
    else:  # Modo original
        file_to_run = os.path.join("./scripts", "botlinkdinW.py" if os_choice == 0 else "botlinkdinL.py")
        stdscr.clear()
        stdscr.addstr(0, 0, f"Running bot for {'Windows' if os_choice == 0 else 'Linux'}...")
        stdscr.refresh()
        subprocess.run(["python", file_to_run, browser_path, profile_path, logged_in])
    
    stdscr.addstr(2, 0, "Bot executed. Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)