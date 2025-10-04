import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import os
import sys
from PIL import Image, ImageTk

try:
    import zenith_monitor as mn 
except ImportError:
    class MockMonitor:
        def start_monitor(self, baseline=None):
            return type('MockObserver', (object,), {'stop': lambda: None, 'join': lambda: None})()
        def load_baseline(self): return {}
        def load_config(self): return {"monitor_paths": ["Caminho de Simulação/Documentos", "Caminho de Simulação/Downloads"]}
        def get_appdata_dir(self): return os.path.expanduser("~")
        def log_event(self, message): print(f"[LOG SIMULADO] {message}")
        LOG_FILE = os.path.join(os.path.expanduser("~"), "zenithguard_simulado.log")
        def __init__(self):
            if not os.path.exists(self.LOG_FILE):
                 with open(self.LOG_FILE, "w") as f: f.write("[SIMULADO] Log de Eventos.\n")
    mn = MockMonitor()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

ZENITH_COLORS = {
    "primary": "#FFD700",
    "secondary": "#333333",
    "background": "#1C1C1C",
    "text": "#EEEEEE",
    "alert": "#FF4500"
}

class ZenithGuardGUI(ctk.CTk):
    def __init__(self, monitor_module):
        super().__init__()
        self.mn = monitor_module
        self.title("ZenithGuardAV")
        self.geometry("900x600")
        self.configure(fg_color=ZENITH_COLORS["background"])

        self.monitoring_active = False
        self.monitor_thread = None
        self.observer = None
        
        self.load_icons()
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, 
                                          width=140, 
                                          corner_radius=0, 
                                          fg_color=ZENITH_COLORS["secondary"])
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, 
                                       text="ZenithGuard", 
                                       image=self.icons.get("shield"),
                                       compound="left",
                                       font=ctk.CTkFont(size=20, weight="bold", slant="italic"),
                                       text_color=ZENITH_COLORS["primary"])
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.dashboard_button = self._create_nav_button(1, "Dashboard", "dashboard", self.icons.get("dashboard"))
        self.logs_button = self._create_nav_button(2, "Logs de Eventos", "logs", self.icons.get("logs"))
        self.settings_button = self._create_nav_button(3, "Configurações", "settings", self.icons.get("settings"))

        self.dashboard_frame = ctk.CTkFrame(self, fg_color=ZENITH_COLORS["background"])
        self.logs_frame = ctk.CTkFrame(self, fg_color=ZENITH_COLORS["background"])
        self.settings_frame = ctk.CTkFrame(self, fg_color=ZENITH_COLORS["background"])

        self.create_dashboard_content()
        self.create_logs_content()
        self.create_settings_content()
        
        self.select_frame_by_name("dashboard")
        
        self.update_logs_periodically()

    def load_icons(self):
        ICON_SIZE = 24
        self.icons = {}
        base_path = os.path.dirname(__file__)
        icon_dir = os.path.join(base_path, "icons")
        
        icon_map = {
            "shield": "icons\\shield.png",
            "dashboard": "icons\\dashboard.png",
            "logs": "icons\\logs.png",
            "settings": "icons\\settings.png",
            "play": "icons\\play.png",
            "stop": "icons\\stop.png",
            "quarantine": "icons\\quarantine.png",
            "folder": "icons\\folder.png",
        }

        for name, filename in icon_map.items():
            full_path = os.path.join(icon_dir, filename)
            try:
                img = ctk.CTkImage(
                    light_image=Image.open(full_path).resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS), 
                    dark_image=Image.open(full_path).resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS), 
                    size=(ICON_SIZE, ICON_SIZE)
                )
                self.icons[name] = img
            except FileNotFoundError:
                self.icons[name] = None
    
    def _create_nav_button(self, row, text, name, icon_image=None):
        button = ctk.CTkButton(self.sidebar_frame, 
                               command=lambda: self.select_frame_by_name(name),
                               text=text, 
                               image=icon_image,
                               compound="left",
                               fg_color="transparent", 
                               hover_color=ZENITH_COLORS["primary"],
                               text_color=ZENITH_COLORS["text"],
                               anchor="w")
        button.grid(row=row, column=0, padx=20, pady=5, sticky="ew")
        return button

    def select_frame_by_name(self, name):
        frames = {"dashboard": self.dashboard_frame, "logs": self.logs_frame, "settings": self.settings_frame}
        buttons = {"dashboard": self.dashboard_button, "logs": self.logs_button, "settings": self.settings_button}

        for btn in buttons.values():
            btn.configure(fg_color="transparent", text_color=ZENITH_COLORS["text"])
        
        for frame_name, frame in frames.items():
            if frame_name == name:
                frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
                buttons[name].configure(fg_color=ZENITH_COLORS["primary"], 
                                        text_color=ZENITH_COLORS["background"], 
                                        hover_color=ZENITH_COLORS["primary"])
            else:
                frame.grid_forget()

    def create_dashboard_content(self):
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(self.dashboard_frame, 
                     text="PAINEL DE CONTROLE", 
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=ZENITH_COLORS["primary"]).grid(row=0, column=0, pady=(0, 20), sticky="w")

        status_frame = ctk.CTkFrame(self.dashboard_frame, fg_color=ZENITH_COLORS["secondary"])
        status_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20), padx=5)
        status_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(status_frame, 
                     text="Status do Monitoramento:", 
                     font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.status_label = ctk.CTkLabel(status_frame, 
                                         text="INATIVO", 
                                         font=ctk.CTkFont(size=18, weight="bold"), 
                                         text_color=ZENITH_COLORS["alert"])
        self.status_label.grid(row=0, column=1, padx=20, pady=10, sticky="e")
        
        action_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        action_frame.grid_columnconfigure((0, 1), weight=1)

        self.start_button = ctk.CTkButton(action_frame, 
                                          text="INICIAR MONITORAMENTO", 
                                          image=self.icons.get("play"),
                                          compound="left",
                                          command=self.toggle_monitoring,
                                          fg_color=ZENITH_COLORS["primary"],
                                          hover_color="#FFA500", 
                                          text_color=ZENITH_COLORS["background"],
                                          font=ctk.CTkFont(weight="bold"))
        self.start_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        ctk.CTkButton(action_frame, 
                      text="ABRIR QUARENTENA", 
                      image=self.icons.get("quarantine"),
                      compound="left",
                      command=self.open_quarantine_folder,
                      fg_color=ZENITH_COLORS["secondary"],
                      hover_color=ZENITH_COLORS["primary"],
                      border_color=ZENITH_COLORS["primary"],
                      border_width=1).grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        ctk.CTkLabel(self.dashboard_frame, 
                     text="Últimos Eventos do Sistema (Visualização Rápida):", 
                     font=ctk.CTkFont(size=16, weight="bold")).grid(row=3, column=0, pady=(10, 5), sticky="w")
        
        self.mini_log_display = ctk.CTkTextbox(self.dashboard_frame, 
                                               state="disabled", 
                                               height=180, 
                                               fg_color=ZENITH_COLORS["secondary"])
        self.mini_log_display.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)


    def toggle_monitoring(self):
        if self.monitoring_active:
            try:
                if self.observer:
                    self.observer.stop()
                
                self.monitoring_active = False
                self.status_label.configure(text="INATIVO", text_color=ZENITH_COLORS["alert"])
                self.start_button.configure(text="INICIAR MONITORAMENTO", fg_color=ZENITH_COLORS["primary"], image=self.icons.get("play"))
                self.mn.log_event("[SERVIÇO] Monitoramento encerrado pelo usuário.")
            except Exception as e:
                messagebox.showerror("ZenithGuard", f"Falha ao encerrar monitoramento: {e}")
        else:
            try:
                self.monitor_thread = threading.Thread(target=self._run_monitor_in_thread, daemon=True)
                self.monitor_thread.start()
                
                self.monitoring_active = True
                self.status_label.configure(text="ATIVO", text_color=ZENITH_COLORS["primary"])
                self.start_button.configure(text="PARAR MONITORAMENTO", fg_color=ZENITH_COLORS["alert"], image=self.icons.get("stop"))
                self.mn.log_event("[SERVIÇO] Monitoramento iniciado pelo usuário.")
            except Exception as e:
                messagebox.showerror("ZenithGuard", f"Falha ao iniciar monitoramento: {e}")
                self.monitoring_active = False

    def _run_monitor_in_thread(self):
        try:
            baseline = self.mn.load_baseline()
            self.observer = self.mn.start_monitor(baseline)
            if self.observer:
                self.observer.join()
        except Exception as e:
            self.mn.log_event(f"[ERRO CRÍTICO THREAD] Falha na thread de monitoramento: {e}")
            self.after(0, lambda: self.status_label.configure(text="ERRO CRÍTICO", text_color=ZENITH_COLORS["alert"]))
            self.after(0, lambda: self.start_button.configure(text="INICIAR MONITORAMENTO", fg_color=ZENITH_COLORS["primary"]))
            self.after(0, lambda: messagebox.showerror("Erro Crítico", f"O serviço de monitoramento falhou: {e}"))

    def open_quarantine_folder(self):
        try:
            quarantine_path = os.path.join(self.mn.get_appdata_dir(), "quarantine")
            os.makedirs(quarantine_path, exist_ok=True)

            if sys.platform == "win32":
                os.startfile(quarantine_path)
            elif sys.platform == "darwin":
                os.system(f'open "{quarantine_path}"')
            else:
                os.system(f'xdg-open "{quarantine_path}"')
            self.mn.log_event(f"[GUI] Pasta de Quarentena aberta: {quarantine_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a pasta de Quarentena. Erro: {e}")

    def create_logs_content(self):
        self.logs_frame.grid_columnconfigure(0, weight=1)
        self.logs_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.logs_frame, 
                     text="LOGS COMPLETOS DO SISTEMA", 
                     image=self.icons.get("logs"),
                     compound="left",
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=ZENITH_COLORS["primary"]).grid(row=0, column=0, pady=(0, 10), sticky="w")

        self.log_display = ctk.CTkTextbox(self.logs_frame, 
                                          state="disabled",
                                          fg_color=ZENITH_COLORS["secondary"],
                                          text_color=ZENITH_COLORS["text"],
                                          wrap="word")
        self.log_display.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkButton(self.logs_frame, 
                      text="Limpar Logs (Exibição)", 
                      command=self.clear_log_display,
                      fg_color=ZENITH_COLORS["secondary"],
                      hover_color=ZENITH_COLORS["primary"],
                      border_color=ZENITH_COLORS["primary"],
                      border_width=1).grid(row=2, column=0, pady=(10, 0), sticky="e")

    def update_logs_periodically(self):
        try:
            log_path = self.mn.LOG_FILE 
            
            if not os.path.exists(log_path):
                open(log_path, 'a').close()

            with open(log_path, 'r') as f:
                logs = f.readlines()
            
            self._update_textbox(self.log_display, logs)

            self._update_textbox(self.mini_log_display, logs[-15:])
            
        except AttributeError:
             pass
        except Exception:
            pass

        self.after(1000, self.update_logs_periodically) 

    def _update_textbox(self, textbox, content_list):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", "".join(content_list))
        textbox.see("end")
        textbox.configure(state="disabled")

    def clear_log_display(self):
        self.log_display.configure(state="normal")
        self.log_display.delete("1.0", "end")
        self.log_display.configure(state="disabled")

    def create_settings_content(self):
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(self.settings_frame, 
                     text="CONFIGURAÇÕES DO SISTEMA", 
                     image=self.icons.get("settings"),
                     compound="left",
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=ZENITH_COLORS["primary"]).grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        paths_frame = ctk.CTkFrame(self.settings_frame, fg_color=ZENITH_COLORS["secondary"])
        paths_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20), padx=5)
        paths_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(paths_frame, 
                     text="Caminhos Monitorados (monitor_paths em config.json):", 
                     font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.path_list_label = ctk.CTkLabel(paths_frame, 
                                            text="Carregando...", 
                                            justify="left", 
                                            anchor="w",
                                            wraplength=700,
                                            text_color=ZENITH_COLORS["text"])
        self.path_list_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        ctk.CTkButton(paths_frame, 
                      text="Abrir Diretório ZenithGuardAV", 
                      image=self.icons.get("folder"),
                      compound="left",
                      command=self.open_appdata_dir,
                      fg_color="transparent",
                      hover_color=ZENITH_COLORS["primary"],
                      border_color=ZENITH_COLORS["primary"],
                      border_width=1).grid(row=2, column=0, padx=10, pady=(10, 10), sticky="e")

        self.load_paths_display()
        
    def load_paths_display(self):
        try:
            config = self.mn.load_config()
            paths = config.get("monitor_paths", ["Nenhum caminho definido."])
            paths_text = "\n".join([f"- {p}" for p in paths])
            self.path_list_label.configure(text=paths_text)
        except Exception:
             self.path_list_label.configure(text="Não foi possível carregar as configurações. Verifique o 'monitor.py'.")

    def open_appdata_dir(self):
        try:
            appdata_path = self.mn.get_appdata_dir()
            os.makedirs(appdata_path, exist_ok=True)
            
            if sys.platform == "win32":
                os.startfile(appdata_path)
            elif sys.platform == "darwin":
                os.system(f'open "{appdata_path}"')
            else:
                os.system(f'xdg-open "{appdata_path}"')
            self.mn.log_event(f"[GUI] Diretório de Configurações aberto: {appdata_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o diretório. Erro: {e}")

if __name__ == "__main__":
    try:
        app = ZenithGuardGUI(mn) 
        app.mainloop()
    except Exception as e:
        print(f"ERRO CRÍTICO DE GUI: {e}")