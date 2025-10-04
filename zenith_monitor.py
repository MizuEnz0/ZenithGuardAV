import os
import json
import hashlib
import shutil
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

try:
    import psutil
except ImportError:
    print("Aviso: 'psutil' não instalado. Funcionalidades de Kill de Processo serão LIMITADAS.")
    psutil = None
try:
    import yara
except ImportError:
    print("Aviso: 'yara-python' não instalado. A detecção YARA não funcionará.")
    yara = None

if os.name == "nt":
    try:
        import ctypes
    except ImportError:
        ctypes = None

def get_appdata_dir():
    if os.name == "nt": 
        base = os.getenv("APPDATA")
    else: 
        base = os.path.expanduser("~/.local/share")
    path = os.path.join(base, "ZenithGuardAV")
    os.makedirs(path, exist_ok=True)
    return path

APPDATA_DIR = get_appdata_dir()
HONEYPOT_DIR = os.path.join(APPDATA_DIR, "honeypots")
QUARANTINE_DIR = os.path.join(APPDATA_DIR, "quarantine")
WL_FILE = os.path.join(APPDATA_DIR, "whitelist.json")
BASELINE_FILE = os.path.join(APPDATA_DIR, "baseline.json")
LOG_FILE = os.path.join(APPDATA_DIR, "zenithguard.log")
CONFIG_FILE = os.path.join(APPDATA_DIR, "config.json")

YARA_RULES_FILENAME = "zenith_rules.yar"
YARA_RULES_FILE = os.path.join(APPDATA_DIR, YARA_RULES_FILENAME)
compiled_rules = None

RATE_LIMIT_SECONDS = 10 
RATE_LIMIT_COUNT = 15 
SYSTEM_FILE_EXCLUSIONS = [
    "desktop.ini", 
    "thumbs.db", 
    ".ds_store",
    "~$" 
]

os.makedirs(HONEYPOT_DIR, exist_ok=True)
os.makedirs(QUARANTINE_DIR, exist_ok=True)

def load_config():
    default = {
        "monitor_paths": [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
        ]
    }
    return default
CONFIG = load_config()
MONITOR_PATHS = CONFIG.get("monitor_paths", [])

def log_event(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

def sha256_file(filepath):
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception:
        return None 

def load_baseline():
    if not os.path.exists(BASELINE_FILE): return {}
    with open(BASELINE_FILE, 'r') as f: return json.load(f)

def load_whitelist():
    if not os.path.exists(WL_FILE): return []
    with open(WL_FILE, 'r') as f: return json.load(f)

def criar_honeypots():
    pass

def mover_para_quarentena(filepath):
    if not os.path.exists(filepath): return
    base = os.path.basename(filepath)
    dest = os.path.join(QUARANTINE_DIR, f"{time.time()}_{base}") 
    try:
        shutil.move(filepath, dest)
        log_event(f"[QUARENTENA] {filepath} -> {dest}")
        return dest
    except Exception as e:
        log_event(f"[ERRO] Falha ao mover para quarentena: {e}")
        return None

def load_yara_rules():
    global compiled_rules
    if not yara: return None
    return compiled_rules

def scan_file_with_yara(filepath):
    return []

def is_admin():
    if os.name == "nt" and ctypes:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    elif os.name != "nt":
        return os.geteuid() == 0
    return False

def kill_process_by_pid(pid):
    if not psutil: return False
    if not is_admin():
        log_event("[PRIVILÉGIO] WARNING: Falha no KILL provável. Rodar como Administrador/root é OBRIGATÓRIO.")
        
    try:
        proc = psutil.Process(pid)
        proc_name = proc.name()
        
        log_event(f"[KILL INICIADO] Tentando encerrar PID {pid} ({proc_name}).")

        proc.terminate()
        time.sleep(0.5) 
        
        if proc.is_running():
            log_event(f"[KILL FORÇADO] Processo {pid} ainda ativo. Enviando KILL -9.")
            proc.kill()
            time.sleep(0.5) 

        if not proc.is_running():
            log_event(f"[SUCESSO KILL] Processo {pid} ({proc_name}) FINALIZADO.")
            return True
        else:
            log_event(f"[FAIL CRÍTICO] Processo {pid} RESISTIU à finalização. Falha de Permissão ou Rootkit.")
            return False      
    except psutil.NoSuchProcess:
        log_event(f"[SUCESSO KILL] Processo {pid} já não existe.")
        return True
    except psutil.AccessDenied:
        log_event(f"[FAIL CRÍTICO] Falha de Permissão ao tentar matar PID {pid}. É necessário rodar como Administrador.")
        return False
    except Exception as e:
        log_event(f"[KILL ERRO GENÉRICO] Falha ao encerrar PID {pid}: {e}")
        return False

def identify_and_kill_process(filepath):
    if not psutil: return False
    log_event(f"[KILL HEURÍSTICA] Buscando processo suspeito ativo...")
    RECENT_THRESHOLD = 15
    HIGH_RISK_PROCS = ["tasksche.exe", "wcry.exe", "taskdl.exe", "taskse.exe", "perfc.dat", "vssadmin.exe"] 
    WHITELISTED_PROCS = ["explorer.exe", "cmd.exe", "powershell.exe", "bash", "zenith_gui.py", "zenith_monitor.py", "python.exe", "pythonw.exe", "svchost.exe", "lsass.exe"]
    target_pid = None
    
    for proc in psutil.process_iter(['pid', 'name', 'create_time', 'cmdline']):
        try:
            name = proc.name().lower()
            if name in HIGH_RISK_PROCS:
                target_pid = proc.pid
                log_event(f"[KILL DETECT - ALTO RISCO] Alvo prioritário encontrado (PID: {target_pid}, Nome: {proc.name()})")
                return kill_process_by_pid(target_pid)
            
            if time.time() - proc.create_time() < RECENT_THRESHOLD:
                if not any(wl_name in name for wl_name in WHITELISTED_PROCS):
                    if name.endswith((".exe", ".py", ".dll")):
                        if target_pid is None:
                            target_pid = proc.pid 
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if target_pid:
        try:
            log_event(f"[KILL DETECT - RECENTE] Alvo heurístico encontrado (PID: {target_pid}, Nome: {psutil.Process(target_pid).name()})")
            return kill_process_by_pid(target_pid)
        except psutil.NoSuchProcess:
            pass

    log_event("[KILL INFO] Nenhuma heurística de Kill recente foi ativada.")
    return False

class DetectorRansomware(FileSystemEventHandler):
    def __init__(self, baseline):
        super().__init__()
        self.baseline = baseline
        self.whitelist = load_whitelist()
        self.modification_timestamps = []
        load_yara_rules()

    def check_rate_limit(self):
        current_time = time.time()
        self.modification_timestamps = [
            t for t in self.modification_timestamps if t > (current_time - RATE_LIMIT_SECONDS)
        ]
        self.modification_timestamps.append(current_time)
        return len(self.modification_timestamps) >= RATE_LIMIT_COUNT

    def process(self, event):
        if event.is_directory:
            return
        path = event.src_path
        name = os.path.basename(path)

        if name.lower() in SYSTEM_FILE_EXCLUSIONS:
            return

        if APPDATA_DIR in path:
            return
            
        sha = sha256_file(path) if os.path.exists(path) else None

        if sha and any(w["sha256"] == sha for w in self.whitelist):
            log_event(f"[WHITELIST] Ignorado {name}")
            return

        is_suspicious_change = False

        if name.startswith("honeypot_") or (sha and sha not in self.baseline.values()):
            log_event(f"[SUSPEITO INTEGRIDADE] {name} modificado/criado. ALTO RISCO.")
            is_suspicious_change = True
            
            if yara and os.path.exists(path) and path.lower().endswith((".exe", ".dll", ".vbs", ".js")):
                yara_matches = scan_file_with_yara(path)
                if yara_matches:
                    rule_names = ", ".join([m.rule for m in yara_matches])
                    log_event(f"[ALERTA YARA MÚLTIPLO] {name} corresponde a regras YARA: {rule_names}. RISCO CRÍTICO.")
                    is_suspicious_change = True 

        if self.check_rate_limit():
            log_event(f"[ALERTA COMPORTAMENTAL] Taxa alta de modificação! ({RATE_LIMIT_COUNT}+ arquivos em {RATE_LIMIT_SECONDS}s).")
            is_suspicious_change = True
            
        if is_suspicious_change:
            log_event(f"[AÇÃO DE BLOQUEIO] Intervenção acionada para {name}.")

            identify_and_kill_process(path) 

            mover_para_quarentena(path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_moved(self, event):
        event.src_path = event.dest_path
        self.process(event)

def start_monitor(baseline):
    event_handler = DetectorRansomware(baseline)
    observer = Observer()

    for path in MONITOR_PATHS:
        if os.path.exists(path):
            observer.schedule(event_handler, path, recursive=True)
            log_event(f"[MONITOR] Iniciado monitoramento em: {path}")
        else:
            log_event(f"[ERRO MONITOR] Caminho não encontrado: {path}")

    observer.start()
    return observer

if __name__ == "__main__":
    if not is_admin():
        print("-" * 50)
        print("!!! ATENÇÃO: EXECUTE ESTA APLICAÇÃO COMO ADMINISTRADOR/ROOT !!!")
        print("Sem privilégios elevados, não será possível encerrar e eliminar atividades suspeitas com sucesso.")
        print("-" * 50)
        
    criar_honeypots()
    baseline = load_baseline() 
    observer = start_monitor(baseline)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    log_event("[MONITOR] Serviço de monitoramento encerrado.")