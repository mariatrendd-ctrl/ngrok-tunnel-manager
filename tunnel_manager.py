"""
T H E - TUNNEL MANAGER v5
Professional TCP Tunnel Orchestrator
"""

import subprocess, threading, time, os, sys, re, random, msvcrt, winsound
import ctypes, struct, socket as _socket
from colorama import init, Fore, Style
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.live import Live
from rich.text import Text
from rich.console import Group
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich import box as rich_box
import urllib.request
import json as _json

init(autoreset=True)
os.system("cls")
os.system("mode con cols=160 lines=60")

try:
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 3)
except Exception:
    pass

# --- Configurations ---
NGROK_EXE      = r"C:\ngrok-v3-stable-windows-amd64\ngrok.exe"
LOG_DIR        = r"C:\ngrok-v3-stable-windows-amd64\endpoints"

# PREENCHA SEUS TOKENS ABAIXO
TOKENS = [
    "", # Token 1
    "", # Token 2
    "", # Token 3
    "", # Token 4
    "", # Token 5
]

NUM_TOKENS      = len(TOKENS)
SLOTS_POR_TOKEN = 3
NUM_SLOTS       = NUM_TOKENS * SLOTS_POR_TOKEN
PORTA_TEMPO     = 1800
CICLO_SLOT      = 15
SPAWN_COOLDOWN  = 0
LIMITE_TCP      = 5000

REGEX = re.compile(r'(\d+\.tcp(?:\.[a-z0-9\-]+)*\.ngrok(?:-free)?\.(?:app|io)):(\d{4,5})', re.IGNORECASE)
console = Console(force_terminal=True, highlight=False, legacy_windows=False, no_color=False)

# --- Global State ---
lock            = threading.Lock()
cache_lock      = threading.Lock()
_tcp_cache      = []
slot_info       = {}
procs           = {}
subindo_set     = set()
conexoes_ativas = {}
letras_usadas   = {}
LETRAS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
slot_t_inicio   = {}
slot_t_spawn    = {}
token_conns_real = [0] * 20
endpoints_usados = set()
endpoints_ja_conectados = set()
blacklist_endpoints = set()
blacklist_flash = {}
token_rate_min = [0] * 20
token_rate_ts = {}

TOKEN_CONNS_FILE = r"C:\ngrok-v3-stable-windows-amd64\token_conns.txt"
ENDPOINTS_USADOS_FILE = r"C:\ngrok-v3-stable-windows-amd64\endpoints_usados.txt"
BLACKLIST_FILE = r"C:\ngrok-v3-stable-windows-amd64\blacklist.txt"

pausado = False
porta_atual = 1000
proxima_porta = 1000
porta_p2 = 1000
tempo_porta = time.time()
tempo_inicio = time.time()
total_conn = 0
_inicio_event = threading.Event()

def _tcp_scan():
    try:
        # Simple netstat wrapper for connection detection
        out = subprocess.check_output(["netstat", "-ano"], text=True, encoding="utf-8", errors="replace")
        rows = []
        for line in out.splitlines():
            if "ESTABLISHED" in line:
                parts = line.split()
                if len(parts) >= 4:
                    rows.append(parts[1])
        return rows
    except: return []

def _thread_tcp():
    global _tcp_cache
    while True:
        try:
            with cache_lock: _tcp_cache = _tcp_scan()
        except: pass
        time.sleep(0.5)

def _spawn(porta, token, api_port):
    cfg = f'version: "2"\nauthtoken: {token}\nweb_addr: 127.0.0.1:{api_port}\n'
    try:
        cfg_path = os.path.join(os.path.dirname(NGROK_EXE), "configs", f"slot_{api_port}.yml")
        os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
        with open(cfg_path, "w", encoding="utf-8") as f: f.write(cfg)
        return subprocess.Popen([NGROK_EXE, "tcp", str(porta), "--config", cfg_path], 
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", bufsize=1)
    except: return None

def _capturar(proc, timeout=22):
    res = [None, None]
    ev = threading.Event()
    def _r():
        try:
            for ln in iter(proc.stdout.readline, ""):
                m = REGEX.search(ln)
                if m:
                    res[0] = m.group(1); res[1] = m.group(2); ev.set(); return
        except: pass
        ev.set()
    threading.Thread(target=_r, daemon=True).start()
    ev.wait(timeout=timeout)
    return res[0], res[1]

def _subir(s, porta):
    if pausado: return
    token = TOKENS[(s-1)//SLOTS_POR_TOKEN] if (s-1)//SLOTS_POR_TOKEN < len(TOKENS) else None
    if not token: return
    
    ap = 4040 + (s-1)*10
    proc = _spawn(porta, token, ap)
    if proc:
        host, p_ep = _capturar(proc)
        if host:
            with lock:
                slot_info[s] = {"status":"online", "host":host, "porta":p_ep}
        else:
            proc.terminate()

def main():
    # Basic loop to start slots
    for i in range(1, NUM_SLOTS + 1):
        threading.Thread(target=_subir, args=(i, 1000 + i), daemon=True).start()
    
    while True:
        os.system("cls")
        print(Panel(f"[bold cyan]T H E - TUNNEL MANAGER v5[/bold cyan]\nStatus: Operacional", expand=False))
        time.sleep(2)

if __name__ == "__main__":
    threading.Thread(target=_thread_tcp, daemon=True).start()
    main()
